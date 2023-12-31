import pandas as pd
import numpy as np
from xgboost import XGBRegressor, XGBClassifier

# list of columns used for variables
list_of_col_run = ['deviceid','segment','length','direction',
'month','day','day_of_week',
'time_of_day',
'dt(n-1)','rt(w-1)','rt(w-2)','rt(w-3)','rt(t-1)','rt(t-2)','rt(n-1)','rt(n-2)','rt(n-3)',
'precip','temp']

bus_run_data = pd.read_csv("data/bus_running_times_feature_added_all.csv")
bus_run_data = bus_run_data.dropna(subset=['run_time_in_seconds'])
bus_run_data = bus_run_data.loc[bus_run_data.direction ==1]

def get_list_cols():
    return list_of_col_run

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
    
def get_run_model(bus_run_data):
    ## Splitting date for training and test data
    date = '2022-10-15'
    train_run = bus_run_data.loc[bus_run_data.date < date]
    test_run = bus_run_data.loc[bus_run_data.date >= date]

    # Training Data
    # Split data into features and target
    train_X_run = train_run[list_of_col_run]
    train_y_run = train_run['run_time_in_seconds']
    # Testing Data
    # Split data into features and target
    test_X_run = test_run[list_of_col_run]
    test_y_run = test_run['run_time_in_seconds']

    # Train a model to predict running times for the next segment
    model_run = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        objective='reg:squarederror',
        random_state=42
    )

    model_run.fit(train_X_run, train_y_run)

    return model_run

def get_run_fea(prev_run_features, prev_dwell_features, prev_dwell, prev_run, week_no):
    features = {key: 0 for key in list_of_col_run}

    features['deviceid'] = prev_dwell_features['deviceid']
    features['segment'] = prev_run_features['segment'] + 1
    features['length'] = search_segment_length(bus_run_data, features['segment'])
    features['direction'] = prev_dwell_features['direction']
    features['month'] = prev_dwell_features['month']
    features['day'] = prev_dwell_features['day']
    features['day_of_week'] = prev_dwell_features['day_of_week']
    features['time_of_day'] = prev_dwell_features['time_of_day']
    features['dt(n-1)'] = prev_dwell
    features['precip'] = prev_dwell_features['precip']
    features['temp'] = prev_dwell_features['temp']
    
    timeslot = features['time_of_day']

    # update rt(t-k) values
    features['rt(t-1)'] = searching_historical_avg_time(bus_run_data, timeslot - 0.25, features['segment'])
    features['rt(t-2)'] = searching_historical_avg_time(bus_run_data, timeslot - 0.5, features['segment'])

    # update rt(w-k) values
    if week_no > 3:
        features['rt(w-1)'] = searching_historical_weekly_avg_time(bus_run_data, week_no - 1, features['segment'], timeslot)
        features['rt(w-2)'] = searching_historical_weekly_avg_time(bus_run_data, week_no - 2, features['segment'], timeslot)
        features['rt(w-3)'] = searching_historical_weekly_avg_time(bus_run_data, week_no - 3, features['segment'], timeslot)
    elif week_no > 2:
        features['rt(w-1)'] = searching_historical_weekly_avg_time(bus_run_data, week_no - 1, features['segment'], timeslot)
        features['rt(w-2)'] = searching_historical_weekly_avg_time(bus_run_data, week_no - 2, features['segment'], timeslot)
        features['rt(w-3)'] = features['rt(w-2)']
    elif week_no > 1:
        features['rt(w-1)'] = searching_historical_weekly_avg_time(bus_run_data, week_no - 1, features['segment'], timeslot)
        features['rt(w-2)'] = features['rt(w-1)']
        features['rt(w-3)'] = features['rt(w-2)']
    else:
        features['rt(w-1)'] = searching_historical_weekly_avg_time(bus_run_data, week_no, features['segment'], timeslot)
        features['rt(w-2)'] = features['rt(w-1)']
        features['rt(w-3)'] = features['rt(w-2)']

    features['rt(n-3)'] = prev_run_features['rt(n-2)']
    features['rt(n-2)'] = prev_run_features['rt(n-1)']
    features['rt(n-1)'] = prev_run

    return features
