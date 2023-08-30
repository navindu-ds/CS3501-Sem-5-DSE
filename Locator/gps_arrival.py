import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import locator

# samp_data_point = {"id":"1227625055","deviceid":121,"devicetime":"2022-07-01 04:26:04",
#                    "latitude":7.29149, "longitude":80.72138,"speed":2.69978}

bus_halts = pd.read_csv('bus_stops_and_terminals_654.csv')

# selecting bus halts from Kandy to Digana 
k2d_halts = bus_halts[:16]

bus_halt_locations = []
for i in k2d_halts.index:
    row = k2d_halts.loc[i]
    location = (row['latitude'], row['longitude'])
    bus_halt_locations.append(location)

# function to use the data_point to check if the bus arrived to its next stop
def is_arrived_next(data_point):
    bus_location = Point((data_point['latitude'], data_point["longitude"]))

    next_stop = max(locator.get_nearest_two_halts(bus_location,  bus_halt_locations))

    return locator.reached_halt(bus_location, next_stop)

# if the bus has arrived returns the arrival time and if not returns None
def check_arrival_time(samp_data_point):
    if (is_arrived_next):
        return samp_data_point['devicetime']
    else:
        return None