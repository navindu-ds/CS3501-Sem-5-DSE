import os
from datetime import time, timedelta
import pandas as pd

from setEnvironment import getApplication

application = getApplication()

from busArrivalTime.models import BusStopTimes

def addStopTime(startTime, endTime):
    dataset = pd.read_csv('data/busses_stop_train.csv')
    dataset.dropna(inplace=True)
    dataset['date'] = pd.to_datetime(dataset['date'])
    dataset['departure_time'] = pd.to_datetime(dataset['departure_time'], format='%H:%M:%S')

    # Sort the DataFrame by "date" and 'departure_time'"
    df_sorted = dataset.sort_values(by=['date', 'departure_time'])

    date_component = dataset['date'].dt.date
    time_component = dataset['departure_time'].dt.time

    # Create a new datetime column by combining the date and time components
    dataset['new_datetime'] = pd.to_datetime(date_component.astype(str) + ' ' + time_component.astype(str))

    # Define the start and end datetime range
    # start_datetime = pd.to_datetime('2021-10-01 06:40:00')
    # end_datetime = pd.to_datetime('2021-10-01 06:50:00')

    start_datetime = startTime
    end_datetime = endTime

    # Create a boolean mask based on the conditions
    mask = (dataset["new_datetime"] >= start_datetime) & (dataset["new_datetime"] <= end_datetime)

    # Apply the mask to filter the DataFrame
    filtered_rows = dataset[mask]
    # Use .loc to assign values without warnings
    filtered_rows.loc[:, 'departure_time'] = filtered_rows['departure_time']


    for index, row in filtered_rows.iterrows():
        # Convert the dwell_time string to a timedelta object
        dwell_time_str = row['dwell_time']
        dwell_time_parts = dwell_time_str.split(':')
        dwell_time = timedelta(hours=int(dwell_time_parts[0]), minutes=int(dwell_time_parts[1]),
                               seconds=int(dwell_time_parts[2]))/1000000

        BusStopTimes.objects.create(
            trip_id=row['trip_id'],
            deviceid=row['deviceid'],
            direction=row['direction'],
            bus_stop=row['bus_stop'],
            date=row['date'],
            arrival_time=row['arrival_time'],
            departure_time=row['departure_time'],
            dwell_time=dwell_time,
            dwell_time_in_seconds_old=row['dwell_time_in_seconds_old'],
            day_of_week=row['day_of_week'],
            time_of_day=row['time_of_day'],
            Sunday_holiday=row['Sunday/holiday'],
            saturday=row['saturday'],
            weekday_end=row['weekday/end'],
            week_no=row['week_no'],
            dt_w_1=row['dt(w-1)'],
            dt_w_2=row['dt(w-2)'],
            dt_w_3=row['dt(w-3)'],
            dt_t_1=row['dt(t-1)'],
            dt_t_2=row['dt(t-2)'],
            dt_n_1=row['dt(n-1)'],
            dt_n_2=row['dt(n-2)'],
            dt_n_3=row['dt(n-3)'],
            hour_of_day=row['hour_of_day'],
            day=row['day'],
            month=row['month'],
            temp=row['temp'],
            precip=row['precip'],
            windspeed=row['windspeed'],
            conditions=row['conditions'],
            rt_n_1=row['rt(n-1)'],
            stop_type=row['stop_type'],
            dwell_time_in_seconds=row['dwell_time_in_seconds'],
        )
