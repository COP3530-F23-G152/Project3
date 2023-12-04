import pandas as pd
import geopandas as gpd
from pandas.io.formats.format import math
import pygame
from shapely.geometry import MultiPolygon, Polygon, Point
from tqdm import tqdm
from AdjacencyMatrixGraph import AdjacencyMatrixGraph
from AdjacencyListGraph import AdjacencyListGraph

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
    backend_text = font.render("Current Backend: Adjacency Matrix Graph", True, (255, 255, 255))
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
                    backend_text = font.render("Current Backend: Adjacency List Graph", True, (255, 255, 255))
                    print("Switched to adjacency list graph")
                if event.key == pygame.K_m:
                    working_graph = matrix_graph
                    backend_text = font.render("Current Backend: Adjacency Matrix Graph", True, (255, 255, 255))
                    print("Switched to adjacency matrix graph")

        screen.fill(BACKGROUND_COLOR)

        if selected:
            # Add one here to stop divide by zero errors
            max_degree = working_graph.max_in(selected) + 1

        for idx, geometry in enumerate(zone_geometries):
            if idx == selected:
                continue
            if idx == hovered:
                continue
            color = min_color
            if selected:
                weight = math.pow(working_graph.count_edges(idx, selected) / max_degree, 0.25)
                color = color_blend(weight, max_color, min_color) 

            draw_zone_geometry(screen, geometry, color, BACKGROUND_COLOR)

        if hovered:
            draw_zone_geometry(screen, zone_geometries[hovered], min_color, (255, 255, 255))
        if selected:
            draw_zone_geometry(screen, zone_geometries[selected], (255, 255, 255), (0, 0, 0))

        screen.blit(font.render("FPS: {:.2f} fps".format(fps_clock.get_fps()), True, (255, 255, 255)), (1400-backend_text.get_size()[0]-20, 10))
        screen.blit(backend_text, (1400-backend_text.get_size()[0]-20, 30))

        # Update the display
        pygame.display.flip()
        fps_clock.tick()

if __name__ == "__main__":
    main() 
