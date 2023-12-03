import pandas as pd
import geopandas as gpd
import time
import pygame
from shapely.geometry import MultiPolygon, Polygon, Point
from AdjacencyListGraph import AdjacencyListGraph

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

def draw_scaled_and_shifted_geometry(screen, geometry, color):
    if geometry.geom_type == 'Polygon':
        draw_scaled_and_shifted_polygon(screen, geometry, color)
    elif geometry.geom_type == 'MultiPolygon':
        for polygon in geometry.geoms:
            draw_scaled_and_shifted_polygon(screen, polygon, color)
            

def draw_scaled_and_shifted_polygon(screen, polygon, color):
    exterior_coords = [(int(x), int(y)) for x, y in polygon.exterior.coords]
    pygame.draw.polygon(screen, color, exterior_coords)
    pygame.draw.polygon(screen, (0, 0, 0), exterior_coords, 1)


def main():
    gdf = gpd.read_file('taxi_zones.shp')
    
    yellow_taxi_df = pd.read_parquet('yellow_tripdata_2023-01.parquet', engine='fastparquet')
    zone_lookup_df = pd.read_csv("taxi+_zone_lookup.csv")

    my_graph = AdjacencyListGraph()
    # get the current time in seconds
    start = time.time()

    for i in zone_lookup_df['LocationID']:
        my_graph.add_vertex(i)

    for i in range(len(yellow_taxi_df)):
        my_graph.add_edge(yellow_taxi_df['DOLocationID'][i], yellow_taxi_df['PULocationID'][i], 1)

    end = time.time()
    print("Time to Create Graph:", end-start)

    # Create a pygame window
    pygame.init()
    screen = pygame.display.set_mode((1200, 1000))
    pygame.display.set_caption("An Interactive Map of")

    # Define the scale factor and shift values (adjust as needed)
    scale_factor = 0.006
    shift_x = -900000 * scale_factor
    shift_y = 127500 * scale_factor
    # Clear the screen
    screen.fill((0, 0, 0))


    # Draw all geometries in the GeoDataFrame
    def drawpolygons(color):
        for geometry in gdf['geometry']:
            scaled_and_shifted_geometry = scale_and_shift_geometry(geometry, scale_factor, shift_x, shift_y)
            draw_scaled_and_shifted_geometry(screen, scaled_and_shifted_geometry, color)

    base_color = (0,185,140)                        
    drawpolygons(base_color)          
                                         
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                screen.fill((0, 0, 0))
                drawpolygons(base_color) 
                i = 0
                for geometry in gdf['geometry']:
                    i += 1
                    scaled_and_shifted_polygon = scale_and_shift_geometry(geometry, scale_factor, shift_x, shift_y)
                    if (scaled_and_shifted_polygon.contains(Point(pygame.mouse.get_pos()))):
                        adjacency_df = my_graph.display_adjacency_list_for_vertex(i)
                        for j in range(len(adjacency_df)):
                            poly = gdf['geometry'].iloc[adjacency_df['Zone'].iloc[j]-1]
                            scaled_and_shifted_polygon = scale_and_shift_geometry(poly, scale_factor, shift_x, shift_y)
                            adjacent_color = (adjacency_df['Red_Value'].iloc[j],0,125) 
                            draw_scaled_and_shifted_geometry(screen, scaled_and_shifted_polygon, adjacent_color)
                        clicked_color = (255,255,255) 
                        scaled_and_shifted_polygon = scale_and_shift_geometry(geometry, scale_factor, shift_x, shift_y)
                        draw_scaled_and_shifted_geometry(screen, scaled_and_shifted_polygon, clicked_color)
                        

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main() 
