import os
import pandas as pd
from setEnvironment import getApplication

application = getApplication()

from busArrivalTime.models import BusRunningTimes

def main():
    filtered_rows = pd.read_csv('data/busses_train.csv')  # Load your filtered data here

    for index, row in filtered_rows.iterrows():
        BusRunningTimes.objects.create(
            trip_id=row['trip_id'],
            deviceid=row['deviceid'],
            direction=row['direction'],
            segment=row['segment'],
            date=row['date'],
            start_time=row['start_time'],
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

    print("Data inserted successfully.")


if __name__ == "__main__":
    main()