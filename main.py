import pandas as pd
import geopandas as gpd
from pandas.io.formats.format import math
import pygame
from shapely import reverse
from shapely.geometry import MultiPolygon, Polygon, Point
from tqdm import tqdm
from AdjacencyMatrixGraph import AdjacencyMatrixGraph
from AdjacencyListGraph import AdjacencyListGraph
from InfoCard import draw_info_card

BACKGROUND_COLOR = (100, 100, 100)

def color_blend(weight, c1, c2):
    c1w = weight
    c2w = 1 - weight
    return (c1[0]*c1w + c2[0]*c2w, c1[1]*c1w + c2[1]*c2w, c1[2]*c1w + c2[2]*c2w)

def scale_and_shift_geometry(geometry, scale_factor, shift_x, shift_y):
    if geometry.geom_type == 'Polygon':
        return scale_and_shift_polygon(geometry, scale_factor, shift_x, shift_y)
    elif geometry.geom_type == 'MultiPolygon':
        polygons = [scale_and_shift_polygon(p, scale_factor, shift_x, shift_y) for p in geometry.geoms]
        return MultiPolygon(polygons)
    else:
        raise ValueError("Unsupported geometry type")

def scale_and_shift_polygon(polygon, scale_factor, shift_x, shift_y):
    # Extract coordinates from the polygon
    coords = list(polygon.exterior.coords)

    # Scale and shift the coordinates, and flip the y-coordinates
    scaled_and_shifted_coords = [
        (int((x * scale_factor) + shift_x), int((900 - (y) * scale_factor) + shift_y))
        for x, y in coords
    ]

    # Return the scaled and shifted polygon
    return Polygon(scaled_and_shifted_coords)

def draw_zone_geometry(screen, geometry, fill_color, border_color):
    if geometry.geom_type == 'Polygon':
        draw_zone_polygon(screen, geometry, fill_color, border_color)
    elif geometry.geom_type == 'MultiPolygon':
        for polygon in geometry.geoms:
            draw_zone_polygon(screen, polygon, fill_color, border_color) 

def draw_zone_polygon(screen, polygon, fill_color, border_color):
    pygame.draw.polygon(screen, fill_color, polygon.exterior.coords)
    pygame.draw.polygon(screen, border_color, polygon.exterior.coords, 1)


def load_adjacency_matrix_graph(zone_lookup, trip_data):
    # add one because the ids are 1 indexed
    graph = AdjacencyMatrixGraph(len(zone_lookup)+1)

    for i in tqdm(range(len(trip_data))):
        graph.add_edge(trip_data['PULocationID'][i], trip_data['DOLocationID'][i])

    return graph

def load_adjacency_list_graph(zone_lookup, trip_data):
    # add one because the ids are 1 indexed
    graph = AdjacencyListGraph(len(zone_lookup)+1)

    for i in tqdm(range(len(trip_data))):
        graph.add_edge(trip_data['PULocationID'][i], trip_data['DOLocationID'][i])

    return graph


def create_polygons(gdf, sw, sh, sox, soy):
    polygons = []

    minx, miny, maxx, maxy = gdf.total_bounds
    x_scale = sw / (maxx-minx)
    y_scale = -sh / (maxy-miny)
    x_off = minx*x_scale - sox
    y_off = maxy*y_scale - soy
    trans_matrix = [x_scale, 0, 0, y_scale, -x_off, -y_off]
    gdf = gdf.affine_transform(trans_matrix)

    polygons.extend(gdf)
    return polygons

def main():
    print("Loading taxi zones...", end=' ', flush=True)
    gdf = gpd.read_file('taxi_zones.shp')
    zone_lookup_df = pd.read_csv("taxi+_zone_lookup.csv")
    print("done!")
 
    print("Creating polygons...", end=' ', flush=True)
    zone_geometries = create_polygons(gdf, 1000, 1000, 200, 0)
    print("done!")
    
    print("Loading trip data...", end=' ', flush=True)
    # yellow_taxi_df = pd.read_parquet('yellow_tripdata_2023-01.parquet', engine='fastparquet')
    yellow_taxi_df = pd.read_parquet('yellow_tripdata_2023-01.parquet', engine='fastparquet').head(100000)
    print("done!")

    print("Loading adjacency matrix graph...")
    matrix_graph = load_adjacency_matrix_graph(zone_lookup_df, yellow_taxi_df)
    print("done!")

    print("Loading adjacency list graph...")
    list_graph = load_adjacency_list_graph(zone_lookup_df, yellow_taxi_df)
    print("done!")

    # Create a pygame window
    pygame.init()
    screen = pygame.display.set_mode((1400, 1000))
    pygame.display.set_caption("An Interactive Map of")
    font = pygame.font.SysFont("Helvetica", 12) 
    # Clear the screen

    min_color = (0, 0, 125)                        
    max_color = (255, 0, 125)
                                         
    # Main game loop
    selected = None
    hovered = None
    working_graph = matrix_graph
    backend_text = "Current Backend: Adjacency Matrix Graph"
    fps_clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                selected = None
                mouse_pos = Point(pygame.mouse.get_pos())
                for idx, zone_geometry in enumerate(zone_geometries):
                    if zone_geometry.contains(mouse_pos):
                        selected = idx

            if event.type == pygame.MOUSEMOTION:
                hovered = None
                mouse_pos = Point(pygame.mouse.get_pos())
                for idx, zone_geometry in enumerate(zone_geometries):
                    if zone_geometry.contains(mouse_pos):
                        hovered = idx
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    working_graph = list_graph
                    backend_text = "Current Backend: Adjacency List Graph"
                if event.key == pygame.K_m:
                    working_graph = matrix_graph
                    backend_text = "Current Backend: Adjacency Matrix Graph"

        screen.fill(BACKGROUND_COLOR)

        if selected:
            # Add one here to stop divide by zero errors
            max_degree = working_graph.max_in(selected) + 1
            total_degree = working_graph.total_in(selected) + 1

        weights = []
        percents = []

        for i in range(len(zone_lookup_df)):
            if selected:
                edges = working_graph.count_edges(i, selected)
                weights.append(math.pow(edges / max_degree, 0.25))
                percents.append((edges / total_degree) * 100)
            else:
                weights.append(0)
                percents.append(0)

        for idx, geometry in enumerate(zone_geometries):
            if idx == selected:
                continue
            if idx == hovered:
                continue
            color = color_blend(weights[idx], max_color, min_color) 

            draw_zone_geometry(screen, geometry, color, BACKGROUND_COLOR)

        if hovered:
            draw_zone_geometry(screen, zone_geometries[hovered], min_color, (255, 255, 255))
        if selected:
            draw_zone_geometry(screen, zone_geometries[selected], (255, 255, 255), (0, 0, 0))

        if hovered:
            mouse_pos = pygame.mouse.get_pos()

            draw_info_card(
                        screen,
                        font,
                        mouse_pos,
                        mouse_pos[0] < 700,
                        mouse_pos[1] < 500,
                        ["{} - {}".format(zone_lookup_df['Zone'][hovered], zone_lookup_df['Borough'][hovered]),
                        "Incoming Percent: {:.2f}%".format(percents[hovered])]
                    )

        draw_info_card(
                    screen,
                    font,
                    (1380, 20),
                    False,
                    True,
                    ["FPS: {:.2f} fps".format(fps_clock.get_fps()),
                     backend_text,]
                )

        rank_data = []
        for i in range(len(zone_lookup_df)):
            rank_data.append((percents[i], "{} - {}".format(zone_lookup_df['Zone'][i], zone_lookup_df['Borough'][i])))

        rank_data.sort(key=lambda x: x[0], reverse=True)
        rank_texts = []

        for rank in rank_data[:25]:
            if rank[0] > 0:
                rank_texts.append("{}: {:.2f}%".format(rank[1], rank[0]))

        draw_info_card(
                    screen,
                    font,
                    (20, 20),
                    True,
                    True,
                    rank_texts
                )

        # Update the display
        pygame.display.flip()
        fps_clock.tick()

if __name__ == "__main__":
    main() 
