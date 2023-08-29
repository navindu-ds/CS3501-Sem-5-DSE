import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

bus_halts = pd.read_csv('bus_stops_and_terminals_654.csv')

# selecting bus halts from Kandy to Digana 
k2d_halts = bus_halts[:16]

bus_halt_locations = []
for i in k2d_halts.index:
    row = k2d_halts.loc[i]
    location = (row['latitude'], row['longitude'])
    bus_halt_locations.append(location)
    
bus_halt_gdf = gpd.GeoDataFrame(geometry=[Point(location) for location in bus_halt_locations])

halt_status = [0]*len(bus_halt_locations)
segment_status = [0]*(len(bus_halt_locations) + 1)

def get_nearest_two_halts(bus_location, bus_halt_locations):
    # Calculate distances to all bus halt locations
    distances = [Point(loc).distance(bus_location) for loc in bus_halt_locations]

    # Find the index of the second smallest distance
    sorted_index = sorted(range(len(distances)), key=lambda i: distances[i])
    first_halt_idx = sorted_index[0]
    second_halt_idx = sorted_index[1]

    return first_halt_idx, second_halt_idx

def clear_halt_status():
    return [0]*(len(bus_halt_locations))

def clear_segment_status():
    return [0]*(len(bus_halt_locations)+1)

def clear_halt_segment_status():
    return clear_halt_status(), clear_segment_status()

def reached_halt(bus_location, halt):
    buffer_radius = 0.0015
    polygon = bus_halt_gdf.loc[halt].geometry.buffer(buffer_radius)
    return polygon.contains(Point(bus_location)) 

def combine_halt_segment_lists(halt_status, segment_status):
    main_list = []
    for i in range(len(segment_status)):
        main_list.append(halt_status[i])
        main_list.append(segment_status[i])
    main_list.append(halt_status[i])
    return main_list

# returns a list of indicators alternating for bus halts and bus segments
    # 0th element - start terminal
    # 1st elemet - segment between start terminal and bus halt 1
    # 2nd element - bus halt 1
    # 3rd element - segment between bus halt 1 and bus halt 2
    # 4th element - bus halt 2
    # and so on...
def get_status_of_bus(bus_location):
    bus_location = Point(bus_location)

    segment = list(get_nearest_two_halts(bus_location, bus_halt_locations))

    next_stop = max(segment)

    if(not(reached_halt(bus_location, next_stop))):
        segment_status , halt_status = clear_halt_segment_status()
        segment_status[min(segment)] = 1
    else:
        segment_status , halt_status = clear_halt_segment_status()
        halt_status[next_stop] = 1
    
    return combine_halt_segment_lists(halt_status, segment_status)