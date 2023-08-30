import numpy as np
import pandas as pd
from xgboost import XGBRegressor, XGBClassifier

# list of columns used for variables
list_of_col = ['deviceid','bus_stop','direction','stop_type',
            'day_of_week','month','day',
            'time_of_day',
            'dt(w-1)','dt(w-2)','dt(w-3)','dt(t-1)','dt(t-2)','dt(n-1)','dt(n-2)','dt(n-3)','rt(n-1)',
            'precip','windspeed']

def get_list_cols():
    return list_of_col

def searching_historical_avg_time(dataset, time_of_day, bus_stop):
    data = pd.DataFrame(dataset.groupby(['time_of_day','bus_stop']).dwell_time_in_seconds.mean())
    return round(data.loc[(time_of_day, bus_stop)][0])

def searching_historical_weekly_avg_time(dataset, week_no, bus_stop, time_of_day):
    data = pd.DataFrame(dataset.groupby(['week_no','bus_stop','time_of_day']).dwell_time_in_seconds.mean())
    try:
        avg_time = data.loc[(week_no, bus_stop, time_of_day)][0]
    except KeyError:
        avg_time = search_nearby_historical(dataset, week_no, bus_stop, time_of_day)
    return round(avg_time)

def search_nearby_historical(dataset, week_no, bus_stop, time_of_day):
    nearby_timeslots = []
    time_slot = time_of_day
    while (time_slot - time_of_day <= 2):
        nearby_timeslots.append(time_slot - 0.25)
        nearby_timeslots.append(time_slot + 0.25)
        time_slot += 0.25

    for nearby_timeslot in nearby_timeslots:
        avg_time = searching_historical_weekly_avg_time(dataset, week_no, bus_stop, nearby_timeslot)
        if avg_time is not None:
            return avg_time

    return None

def search_stop_type(dataset, bus_stop):
    data = pd.DataFrame(dataset.groupby('bus_stop').stop_type.unique().apply(lambda x: x[0]))
    try:
        return data.loc[bus_stop][0]
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
def get_last_stop(bus_stop):
    if bus_stop <= 114:
        return 114
    else:
        return None
    
def get_dwell_models(bus_stop_data):
    date = '2022-10-15'
    train = bus_stop_data.loc[bus_stop_data.date < date]
    test = bus_stop_data.loc[bus_stop_data.date >= date]
        
    # Training Data
    # Split data into features and target
    train_X = train[list_of_col]
    train_y = train['dwell_time_in_seconds']

    # Testing Data
    # Split data into features and target
    test_X = test[list_of_col]
    test_y = test['dwell_time_in_seconds']

    classifier = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        objective='reg:squarederror',
        random_state=42)

    classifier.fit(train_X, np.where(train_y > 0 , 1, 0))

    cl_train_y_pred = classifier.predict(train_X)

    train_X_reg = train_X.loc[cl_train_y_pred == 1]
    train_y_reg = train_y.loc[cl_train_y_pred == 1]

    # Train a model to predict dwell times for the next segment
    reg_model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        objective='reg:squarederror',
        random_state=42
    )

    reg_model.fit(train_X_reg, train_y_reg)

    return classifier, reg_model