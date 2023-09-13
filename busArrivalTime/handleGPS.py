import random
import pandas as pd
def getGPSData(bus, time):
    # Generate a random number between 7.2 and 7.3
    lat = random.uniform(7.2, 7.3)

    # Generate a random number between 80.6 and 80.7
    lon = random.uniform(80.6, 80.7)

    # Return the generated numbers as a tuple
    return (lat, lon)

def getLocations():
    dataset = pd.read_csv('data/busses_train.csv')
    return dataset
