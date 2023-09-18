from datetime import datetime, timedelta
from routeDetails import *

def generatePredictions(segment, start_time):
    # Check if start_time is a string
    if isinstance(start_time, str):
        # Convert start_time to datetime object
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    start_time += timedelta(minutes=5)
    # Initialize the dictionary with the first segment and start_time
    arrivalTimes = dict()

    for seg in busStops[:int(segment)-1]:
        # Add new segment and time to dictionary
        arrivalTimes[seg] = 'passed'

    # Generate the rest of the segments
    for seg in busStops[int(segment)-1:]:

        # Add new segment and time to dictionary
        arrivalTimes[seg] = start_time.strftime('%H:%M:%S')
        # Increase time by 1 minute
        start_time += timedelta(minutes=1)


    return arrivalTimes
