# data handling
import numpy as np
import pandas as pd

# data visualizations
import seaborn as sns
import matplotlib.pyplot as plt

# feature scaling
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# feature selection
from sklearn.feature_selection import RFE

# machine learning algorithms
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor, XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import naive_bayes
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.neural_network import MLPClassifier

# Import label encoder
from sklearn.preprocessing import LabelEncoder

# dimensionality reduction with PCA
from sklearn.decomposition import PCA

# accuracy metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, accuracy_score

# date and time handling
import datetime

# helper functions
import run_time_helper, dwell_time_helper

bus_run_data = pd.read_csv("data/bus_running_times_feature_added_all.csv")
bus_stop_data = pd.read_csv("data/bus_stop_times_feature_added_all.csv")

bus_run_data = bus_run_data.dropna(subset=['run_time_in_seconds'])
bus_run_data = bus_run_data.loc[bus_run_data.direction ==1]

label_encoder = LabelEncoder()
bus_stop_data['stop_type'] = label_encoder.fit_transform(bus_stop_data['stop_type'])

model_run = run_time_helper.get_run_model(bus_run_data)
classifier_dwell , reg_dwell = dwell_time_helper.get_dwell_models(bus_stop_data)

def predict_next_run(features):
    list_of_col = run_time_helper.get_list_cols()

    max_stop = run_time_helper.get_last_segment(features['segment'])

    timeslot = features['time_of_day']
    curr_time = pd.to_datetime(features['start_time'])
    week_no = features['week_no']

    # forming the data to be sent for model prediction
    features = {key: features[key] for key in list_of_col}

    return round(model_run.predict(pd.DataFrame([features]))[0])

def predict_next_dwell(features):
    list_of_cols = dwell_time_helper.get_list_cols()

    max_stop = dwell_time_helper.get_last_stop(features['bus_stop'])

    timeslot = features['time_of_day']  
    curr_time = pd.to_datetime(features['arrival_time'])
    week_no = features['week_no']    

    # forming the data to be sent for model prediction
    features = {key: features[key] for key in list_of_cols}

    # apply prediction and save to list
    predicted_time = apply_dwell_time_prediction(pd.DataFrame(features, index={0}))
    return round(max(0, predicted_time))

def apply_dwell_time_prediction(features):
    # applying classifier
    if classifier_dwell.predict(features)[0] == 1:
        return reg_dwell.predict(features)[0]
    else:
        return 0