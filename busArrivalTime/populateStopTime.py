import os
from datetime import time, timedelta

import pandas as pd
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busArrivalTime.settings')
application = get_wsgi_application()

from busArrivalTime.models import BusStopTimes


def main():
    filtered_rows = pd.read_csv('data/busses_stop_train.csv')  # Load your filtered data here

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
            arrival_time=time.fromisoformat(row['arrival_time']),
            departure_time=time.fromisoformat(row['departure_time']),
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
    print("Data inserted successfully.")


if __name__ == "__main__":
    main()
