import numpy as np
import pandas as pd
from datetime import timedelta
from routeDetails import *
from setEnvironment import getApplication
from generatePredictions import generatePredictions
application = getApplication()
from handleGPS import getGPSData, getLocations
from busArrivalTime.models import ArrivalTimes


def getPredictions(segment,start_time, run, dwell):
    return generatePredictions(segment,start_time, run, dwell)

def addRecord(startTime, endTime, run, dwell):
    dataset = getLocations()
    dataset.dropna(inplace=True)
    dataset['date'] = pd.to_datetime(dataset['date'])
    dataset['start_time'] = pd.to_datetime(dataset['start_time'], format='%H:%M:%S')

    # Sort the DataFrame by "date" and "start_time"
    df_sorted = dataset.sort_values(by=['date', 'start_time'])

    date_component = dataset['date'].dt.date
    time_component = dataset['start_time'].dt.time

    # Create a new datetime column by combining the date and time components
    dataset['new_datetime'] = pd.to_datetime(date_component.astype(str) + ' ' + time_component.astype(str))

    # Define the start and end datetime range
    # start_datetime = pd.to_datetime('2021-10-01 06:40:00')
    # end_datetime = pd.to_datetime('2021-10-01 06:50:00')

    start_datetime = startTime
    end_datetime = endTime

    # Create a boolean mask based on the conditions
    mask = (dataset["new_datetime"] >= start_datetime) & (dataset["new_datetime"] <= end_datetime) & (dataset["segment"] == first_segment)

    # Apply the mask to filter the DataFrame
    filtered_rows = dataset[mask]

    if len(filtered_rows) > 0:
        print(filtered_rows)

        arrivalTimes = getPredictions(first_segment,startTime, run, dwell)

        for index, row in filtered_rows.iterrows():
            latitude,longitude = getGPSData(row['deviceid'],startTime)
            arrival_time_data = {
                'trip_id': row['trip_id'],
                'latitude': latitude,
                'longitude': longitude,
                'deviceid': row['deviceid'],
            }
            for stop, time in arrivalTimes.items():
                arrival_time_data[f'{stop}'] = time
            ArrivalTimes.objects.create(**arrival_time_data)

def deleteRecord(startTime, endTime, run, dwell):
    dataset = getLocations()
    dataset.dropna(inplace=True)
    dataset['date'] = pd.to_datetime(dataset['date'])
    dataset['end_time'] = pd.to_datetime(dataset['end_time'], format='%H:%M:%S')

    # Sort the DataFrame by "date" and "end_time"
    df_sorted = dataset.sort_values(by=['date', 'end_time'])

    date_component = dataset['date'].dt.date
    time_component = dataset['end_time'].dt.time

    # Create a new datetime column by combining the date and time components
    dataset['new_datetime'] = pd.to_datetime(date_component.astype(str) + ' ' + time_component.astype(str))

    start_datetime = startTime
    end_datetime = endTime

    # Create a boolean mask based on the conditions
    mask = (dataset["new_datetime"] >= start_datetime) & (dataset["new_datetime"] <= end_datetime) & (
                dataset["segment"] == last_segment)

    # Apply the mask to filter the DataFrame
    filtered_rows = dataset[mask]

    if len(filtered_rows) > 0:
        print(filtered_rows)

        # Get the trip_ids from filtered_rows
        trip_ids_to_delete = filtered_rows['trip_id'].tolist()

        # Delete rows from arrival_times where trip_id is in trip_ids_to_delete
        ArrivalTimes.objects.filter(trip_id__in=trip_ids_to_delete).delete()


def updateRecord(startTime, endTime, run, dwell):
    dataset = getLocations()
    dataset.dropna(inplace=True)
    dataset['date'] = pd.to_datetime(dataset['date'])
    dataset['start_time'] = pd.to_datetime(dataset['start_time'], format='%H:%M:%S')

    # Sort the DataFrame by "date" and "start_time"
    df_sorted = dataset.sort_values(by=['date', 'start_time'])

    date_component = dataset['date'].dt.date
    time_component = dataset['start_time'].dt.time

    # Create a new datetime column by combining the date and time components
    dataset['new_datetime'] = pd.to_datetime(date_component.astype(str) + ' ' + time_component.astype(str))

    # Define the start and end datetime range
    # start_datetime = pd.to_datetime('2021-10-01 06:40:00')
    # end_datetime = pd.to_datetime('2021-10-01 06:50:00')

    start_datetime = startTime
    end_datetime = endTime
    # Create a boolean mask based on the conditions
    mask = (dataset["new_datetime"] >= start_datetime) & (dataset["new_datetime"] <= end_datetime) & (
                dataset["segment"] != first_segment)

    # Apply the mask to filter the DataFrame
    filtered_rows = dataset[mask]

    if len(filtered_rows) > 0:
        print(filtered_rows)

        for index, row in filtered_rows.iterrows():
            latitude, longitude = getGPSData(row['deviceid'], startTime)
            arrival_time_data = {
                'trip_id': row['trip_id'],
                'latitude': latitude,
                'longitude': longitude,
            }
            arrivalTimes = getPredictions(row['segment'],startTime, run, dwell)
            for stop, time in arrivalTimes.items():
                arrival_time_data[f'{stop}'] = time
            ArrivalTimes.objects.filter(trip_id=row['trip_id']).update(**arrival_time_data)

def updateLocations(startTime):
    #get all rows of ArrivalTimes
    arrivalTimes = ArrivalTimes.objects.all()
    # change latitude and longitude of each row by calling getGPSData
    for arrivalTime in arrivalTimes:
        latitude, longitude = getGPSData(arrivalTime.deviceid, startTime)
        arrivalTime.latitude = latitude
        arrivalTime.longitude = longitude
        arrivalTime.save()