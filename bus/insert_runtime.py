import numpy as np
import pandas as pd
from datetime import timedelta
import os
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus.settings')
application = get_wsgi_application()
from bus.models import BusRunningTimes

def addRunningTime(startTime, endTime):

    dataset = pd.read_csv('busses_train.csv')
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
    mask = (dataset["new_datetime"] >= start_datetime) & (dataset["new_datetime"] <= end_datetime)

    # Apply the mask to filter the DataFrame
    filtered_rows = dataset[mask]



    for index, row in filtered_rows.iterrows():
        BusRunningTimes.objects.create(
            trip_id=row['trip_id'],
            deviceid=row['deviceid'],
            direction=row['direction'],
            segment=row['segment'],
            date=row['date'],
            start_time=row['start_time'].time(),
            end_time=row['end_time'],
            run_time_in_seconds=row['run_time_in_seconds'],
            length=row['length'],
            day_of_week=row['day_of_week'],
            time_of_day=row['time_of_day'],
            Sunday_holiday=row['Sunday/holiday'],
            saturday=row['saturday'],
            weekday_end=row['weekday/end'],
            week_no=row['week_no'],
            rt_w_1=row['rt(w-1)'],
            rt_w_2=row['rt(w-2)'],
            rt_w_3=row['rt(w-3)'],
            rt_t_1=row['rt(t-1)'],
            rt_t_2=row['rt(t-2)'],
            rt_n_1=row['rt(n-1)'],
            rt_n_2=row['rt(n-2)'],
            rt_n_3=row['rt(n-3)'],
            hour_of_day=row['hour_of_day'],
            day=row['day'],
            month=row['month'],
            temp=row['temp'],
            precip=row['precip'],
            windspeed=row['windspeed'],
            conditions=row['conditions'],
            dt_n_1=row['dt(n-1)'],
        )

