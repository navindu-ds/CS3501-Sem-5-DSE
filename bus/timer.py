from get_runtime_pred import getRunTimePrediction
from get_dwelltime_pred import getDwellTimePrediction
from insert_run_stop import addData
from keras.models import load_model
import pandas as pd
from datetime import datetime, timedelta
import time
from addPredictions import addRunTimePrediction, addDwellTimePrediction

import mysql.connector

def clear_predictions_tables():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "ch1965298th",
        "database": "bus"
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    tables_to_clear = ["bus_run_time_predictions", "bus_dwell_time_predictions"]

    for table in tables_to_clear:
        query = f"DELETE FROM {table}"
        cursor.execute(query)
        conn.commit()
        print(f"Cleared data from {table} table.")

    cursor.close()
    conn.close()


# Set starting time and date
start_time = datetime.strptime('07:00:00', '%H:%M:%S').time()
start_date = datetime.strptime('2021-10-02', '%Y-%m-%d')

# Loop through 5-minute intervals
current_time = datetime.combine(start_date, start_time)
end_of_day = datetime.combine(start_date, datetime.strptime('23:59:59', '%H:%M:%S').time())

hour = 6
minute = 0
second = 0
k = 100
interval = 1

run_model = load_model('ConvLSTM_runTime.h5')
dwell_model = load_model('ConvLSTM_dwell_time.h5')

run_time_pred = None
dwell_time_pred = None

while current_time <= end_of_day:
    end_time = current_time + timedelta(minutes=interval)

    # Define the start and end datetime range
    start_datetime = current_time
    end_datetime = end_time

    # do stuff here ---------------------------

    addData(start_datetime, end_datetime)

    minutes_since_start = (current_time - start_date).seconds // 60
    if minutes_since_start % 15 == 0:
        # Subtract 8 hours from the current time
        new_datetime = current_time - timedelta(hours=8)

        # Convert the new datetime to a string
        new_datetime_str = new_datetime.strftime('%Y-%m-%d %H:%M:%S')
        # run_time_pred = getRunTimePrediction(run_model, new_datetime_str, str(current_time))
        clear_predictions_tables()
        addRunTimePrediction(run_model,new_datetime_str, str(current_time))
        addDwellTimePrediction(dwell_model,new_datetime_str, str(current_time))
        print(current_time)

    print("Current time: " + str(current_time), minute, second)

    #------------------------------
    current_time = end_time

    second += 1
    time.sleep(interval * 60 * (1 / k))
    if second == 60:
        second = 0
        minute += 1
        if minute == 60:
            minute = 0
            hour += 1
            if hour == 24:
                hour = 0

print("Task completed.")
