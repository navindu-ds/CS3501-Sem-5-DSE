from keras.models import load_model
import pandas as pd
from datetime import datetime, timedelta
import time
from databaseDetails import database
import mysql.connector
from UpdateDateTime import updateTime
from insert_run_stop import addData
from updateArrivalTime import addRecord,deleteRecord,updateRecord,updateLocations

def timer():
    print("Timer started.")
    # Set starting time and date
    start_time = datetime.strptime('10:18:00', '%H:%M:%S').time()
    start_date = datetime.strptime('2021-10-02', '%Y-%m-%d')

    # Loop through 5-minute intervals
    current_time = datetime.combine(start_date, start_time)
    end_of_day = datetime.combine(start_date, datetime.strptime('23:59:59', '%H:%M:%S').time())

    hour = 6
    minute = 0
    second = 0
    k =100
    interval = 1


    while current_time <= end_of_day:
        end_time = current_time + timedelta(minutes=interval)

        # Define the start and end datetime range
        start_datetime = current_time
        end_datetime = end_time

        # do stuff here ---------------------------

        print("Current time: " + str(current_time), minute, second)
        updateTime(str(current_time), str(start_date))
        addRecord(start_datetime, end_datetime)
        deleteRecord(start_datetime, end_datetime)
        updateRecord(start_datetime, end_datetime)
        updateLocations(start_datetime)
        addData(start_datetime, end_datetime)
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

