import pandas as pd
import numpy as np

def searching_historical(data, time_of_day, segment):
    try:
        return round(data.loc[(time_of_day, segment)][0])
    except KeyError:
        return None
    
def searching_historical_avg_time(dataset, time_of_day, segment):
    data = pd.DataFrame(dataset.groupby(['time_of_day','segment']).run_time_in_seconds.mean())
    avg_time = searching_historical(data, time_of_day, segment)
    if avg_time != None:
        return avg_time
    else:
        nearby_timeslots = [time_of_day - 0.25, time_of_day + 0.25, time_of_day - 0.5, time_of_day + 0.5]
        for t in nearby_timeslots:
            avg_time = searching_historical(data, t, segment)
            if avg_time != None:
                return avg_time
        data2 = pd.DataFrame(dataset.groupby(['segment']).run_time_in_seconds.mean())
        return round(data.loc[segment][0])

def searching_historical_weekly_avg_time(dataset, week_no, segment, time_of_day):
    data = pd.DataFrame(dataset.groupby(['week_no','segment','time_of_day']).run_time_in_seconds.mean())
    try:
        avg_time = data.loc[(week_no, segment, time_of_day)][0]
    except KeyError:
        avg_time = search_nearby_historical(dataset, week_no, segment, time_of_day)

    if avg_time != None:
        return round(avg_time)
    else:
        return searching_historical_avg_time(dataset, time_of_day, segment)
    
def searching_historical_weekly(dataset, week_no, segment, time_of_day):
    data = pd.DataFrame(dataset.groupby(['week_no','segment','time_of_day']).run_time_in_seconds.mean())
    try:
        avg_time = data.loc[(week_no, segment, time_of_day)][0]
    except KeyError:
        return None
    return round(avg_time)

def search_nearby_historical(dataset, week_no, segment, time_of_day):
    nearby_timeslots = []
    time_slot = time_of_day
    while (time_slot - time_of_day <= 2):
        nearby_timeslots.append(time_slot - 0.25)
        nearby_timeslots.append(time_slot + 0.25)
        time_slot += 0.25

    for nearby_timeslot in nearby_timeslots:
        avg_time = searching_historical_weekly(dataset, week_no, segment, nearby_timeslot)
        if avg_time is not None:
            return avg_time

    return None

def search_segment_length(dataset, segment_id):
    data = pd.DataFrame(dataset.groupby('segment').length.unique().apply(lambda x: x[0]))

    try:
        return data.loc[segment_id][0]
    except KeyError:
        return None
    
# function to convert time_object into hours in integer form
def time_to_hour(time_obj):
    # the hour part as integer
    decimal_hour = time_obj.hour

    # adding the minute portion as the decimal portion
    if time_obj.minute < 15:
        decimal_hour += 0
    elif time_obj.minute < 30:
        decimal_hour += 0.25
    elif time_obj.minute < 45:
        decimal_hour += 0.5
    else:
        decimal_hour += 0.75
    return decimal_hour

# obtaining the last segment to calculate
def get_last_segment(segment):
    if segment <= 15:
        return 15
    elif segment <= 34:
        return 34
    else:
        return None