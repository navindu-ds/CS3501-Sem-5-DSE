from django.db import models
import os
import sys

# Add the path to the directory containing getArrivalTimes.py
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(rootPath)

from routeDetails import *

class BusRunningTimes(models.Model):
    trip_id = models.FloatField()
    deviceid = models.FloatField()
    direction = models.FloatField()
    segment = models.FloatField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    run_time_in_seconds = models.FloatField()
    length = models.FloatField()
    day_of_week = models.FloatField()  # Update this field's type if needed
    time_of_day = models.FloatField()
    Sunday_holiday = models.FloatField()  # Update this field's name and type if needed
    saturday = models.IntegerField()
    weekday_end = models.IntegerField()
    week_no = models.FloatField()
    rt_w_1 = models.FloatField()  # Update this field's name
    rt_w_2 = models.FloatField()  # Update this field's name
    rt_w_3 = models.FloatField()  # Update this field's name
    rt_t_1 = models.FloatField()  # Update this field's name
    rt_t_2 = models.FloatField()  # Update this field's name
    rt_n_1 = models.FloatField()  # Update this field's name
    rt_n_2 = models.FloatField()  # Update this field's name
    rt_n_3 = models.FloatField()  # Update this field's name
    hour_of_day = models.FloatField()
    day = models.FloatField()
    month = models.FloatField()
    temp = models.FloatField()
    precip = models.FloatField()
    windspeed = models.FloatField()
    conditions = models.CharField(max_length=255)  # Update the max length if needed
    dt_n_1 = models.FloatField()  # Update this field's name

    class Meta:
        db_table = 'bus_running_times'  # Set the table name to match your MySQL table

    def __str__(self):
        return f"BusRunningTimes entry for Trip {self.trip_id}"

class BusStopTimes(models.Model):
    trip_id = models.IntegerField()
    deviceid = models.IntegerField()
    direction = models.IntegerField()
    bus_stop = models.IntegerField()
    date = models.DateField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    dwell_time = models.DurationField()
    dwell_time_in_seconds_old = models.FloatField()
    day_of_week = models.IntegerField()
    time_of_day = models.FloatField()
    Sunday_holiday = models.IntegerField()
    saturday = models.IntegerField()
    weekday_end = models.IntegerField()
    week_no = models.IntegerField()
    dt_w_1 = models.FloatField()
    dt_w_2 = models.FloatField()
    dt_w_3 = models.FloatField()
    dt_t_1 = models.FloatField()
    dt_t_2 = models.FloatField()
    dt_n_1 = models.FloatField()
    dt_n_2 = models.FloatField()
    dt_n_3 = models.FloatField()
    hour_of_day = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    temp = models.FloatField()
    precip = models.FloatField()
    windspeed = models.FloatField()
    conditions = models.CharField(max_length=100)
    rt_n_1 = models.FloatField()
    stop_type = models.CharField(max_length=10)
    dwell_time_in_seconds = models.FloatField()

    def __str__(self):
        return f"BusStopTimes: {self.trip_id} - {self.date} - {self.bus_stop}"

    class Meta:
        db_table = 'bus_stop_times'  # Set the table name to match your MySQL table


class DateAndTime(models.Model):
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        db_table = 'date_and_time'

class ArrivalTimes(models.Model):
    trip_id = models.IntegerField()
    latitude = models.FloatField(default=7.292462226)
    longitude = models.FloatField(default=80.6349778)
    deviceid = models.IntegerField(default=0)
    def __str__(self):
        return f"ArrivalTimes: {self.trip_id} - {self.date} - {self.bus_stop}"

    class Meta:
        db_table = 'arrival_times'

for stop in busStops:
    ArrivalTimes.add_to_class(f'{stop}', models.CharField(max_length=255))