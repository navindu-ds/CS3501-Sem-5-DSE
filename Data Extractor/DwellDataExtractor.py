import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")
import os

from sklearn.preprocessing import MinMaxScaler

current_folder = os.path.abspath('')
dataSet_location = os.path.join(current_folder,'Datasets')
dwellTimeFile = os.path.join(dataSet_location,'bus_stop_times_feature_added_all.csv')

initial_df = pd.read_csv(dwellTimeFile)

busses_new = initial_df[['trip_id','deviceid','direction','bus_stop','date','arrival_time','departure_time','dwell_time','dwell_time_in_seconds']]

# since there are missing data in the Dwell times data table - they will be dropped
busses_new.dropna(inplace=True)

# parameters to generate the average dwell times
bus_stops = 14 # number of bus stops in the route 
time_step = 15 # in minutes
previous_steps = 16 # number of time steps used to predict 
pred_steps = 2 # number of time steps to predict
min = 0
direction = 1
start_time = '06:00:00' # starting time of the time slots
end_time = '19:00:00' # ending time of the time slots

def getAvgDwelltimeWithStop(dataframe, time_step, start_time, end_time, min):
    dataframe = dataframe.copy()
    
    # Convert to datetime objects
    dataframe['departure_time'] = pd.to_datetime(dataframe['departure_time'])
    
    start_time = pd.to_datetime(start_time).time()
    end_time = pd.to_datetime(end_time).time()

    # Create a list to store the data for the new dataframe
    data = []

    # Iterate over the unique dates in the 'date' column
    for date in dataframe['date'].unique():
        # Filter the rows for the current date
        df_date = dataframe[dataframe['date'] == date]
        df_date.loc[:, 'departure_time'] = df_date['departure_time'].dt.time  # Use .loc to modify the original DataFrame
        date = date + pd.Timedelta(minutes=min)
        # Create a time range for the current date with the specified time step
        time_range = pd.date_range(date, date + pd.Timedelta(days=1), freq=f'{time_step}T')

        # Iterate over the time range
        for start, end in zip(time_range[:-1], time_range[1:]):
            # Check if the start time is within the specified time window
            if start.time() >= start_time and start.time() < end_time:
                # Filter the rows for the current time window
                mask = (df_date['departure_time'] >= start.time()) & (df_date['departure_time'] < end.time())
                df_time_window = df_date[mask]
                # Calculate the average dwell time for each bus stop in the current time window
                avg_run_time = df_time_window.groupby('bus_stop')['dwell_time_in_seconds'].mean().reset_index()

                # Append the data to the data list
                for row in avg_run_time.itertuples():
                    data.append((date, start.time(), row.bus_stop, row.dwell_time_in_seconds))

    # Create a new dataframe from the data list
    df_avg_dwell_time = pd.DataFrame(data, columns=['date', 'arrival_time', 'bus_stop', 'avg_dwell_time'])
    return df_avg_dwell_time

def fillTimeSteps(df_avg_dwell_time, startTime, endTime, time_step, num_stops):
    start_Time = pd.to_datetime(startTime).time()

    end_Time = pd.to_datetime(endTime).time()
    # Create a new DataFrame to store the missing data
    data = []

    # Iterate over the unique dates in the 'date' column
    for date in df_avg_dwell_time['date'].unique():
        # Filter the rows for the current date
        df_date = df_avg_dwell_time[df_avg_dwell_time['date'] == date]

        # Create a time range for the current date with the specified time step
        time_range = pd.date_range(date, date + pd.Timedelta(days=1), freq=f'{time_step}T').time

        # Iterate over the time range
        for t in time_range:
            # Check if the start time is within the specified time window
            if start_Time <= t < end_Time:
                # Check if the current start time is present in the dataframe
                if not (df_date['arrival_time'] == t).any():
                    # Add rows for the missing start time and bus stops
                    for stop in range(1, num_stops + 1):
                        data.append((date, t, stop, 0))

    # Create a new DataFrame from the data list
    df_missing = pd.DataFrame(data, columns=['date', 'arrival_time', 'stop', 'avg_dwell_time'])

    # Concatenate the new DataFrame with the original DataFrame
    df_avg_dwell_time = pd.concat([df_avg_dwell_time, df_missing], ignore_index=True)
    # Sort the rows of the dataframe by the 'date', 'arrival_time', and 'bus_stop' columns
    df_avg_dwell_time = df_avg_dwell_time.sort_values(by=['date', 'arrival_time', 'stop'])
    return df_avg_dwell_time

# creating a mask to select only a data regarding the direction 
mask = (busses_new['direction'] == direction)

# selecting the data for the selected direction
busses_new = busses_new[mask]

# Convert the 'date' column to a datetime object
busses_new['date'] = pd.to_datetime(busses_new['date'])

# Create a boolean mask to filter rows with dates on or after 10/1/2022
date_mask = busses_new['date'] >= '2022-10-01'

# Create the train and test dataframes
busses_train = busses_new[~date_mask]
busses_test = busses_new[date_mask]

# obtaining dataframe with average dwell times for each time and stop
df_avg_dwell_time = getAvgDwelltimeWithStop(busses_train,time_step,start_time,end_time,min)

# Create a MultiIndex with all combinations of date, start_time, and stop
idx = pd.MultiIndex.from_product([df_avg_dwell_time['date'].unique(), df_avg_dwell_time['arrival_time'].unique(), 
                                  range((direction*100 + 1), direction*100 + bus_stops + 1)],
                                  names=['date', 'arrival_time', 'bus_stop'])

# Reindex the dataframe using the new MultiIndex
df = df_avg_dwell_time.set_index(['date', 'arrival_time', 'bus_stop']).reindex(idx, fill_value=0).reset_index()

df = fillTimeSteps(df, start_time, end_time, time_step, bus_stops)

# Pivot the DataFrame
pivoted_df = df.pivot_table(index=['date', 'arrival_time'], columns='bus_stop', values='avg_dwell_time', aggfunc='first')

avg_dwell_df = pivoted_df.reset_index()
avg_dwell_df['date'] = avg_dwell_df.apply(lambda x: pd.datetime.combine(x['date'], x['arrival_time']), axis=1)
avg_dwell_df = avg_dwell_df.drop("arrival_time",axis=1)

# file location to save Dataset
filename = 'avg_dwell_dir' + str(direction) + '.csv'
processed_data_file = os.path.join(dataSet_location, filename)

avg_dwell_df.to_csv(processed_data_file,index=False)