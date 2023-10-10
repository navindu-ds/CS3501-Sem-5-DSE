import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")
import os

from sklearn.preprocessing import MinMaxScaler

current_folder = os.path.abspath('')
dataSet_location = os.path.join(current_folder,'Datasets')
runningTimeFile = os.path.join(dataSet_location,'bus_running_times_feature_added_all.csv')

initial_df = pd.read_csv(runningTimeFile)

busses_new = initial_df[['trip_id','deviceid','direction','segment','date','start_time','end_time','run_time','run_time_in_seconds']]

# since there are missing data in the running times data table - they will be dropped
busses_new.dropna(inplace=True)

# parameters to generate the average running times
segments = 15 # number of segments in the route 
time_step = 15 # in minutes
# previous_steps = 16 # number of time steps used to predict 
# pred_steps = 2 # number of time steps to predict
min = 0
direction = 1
start_time = '06:00:00' # starting time of the time slots
end_time = '19:00:00' # ending time of the time slots

def getAvgRuntimeWithSegment(dataframe, time_step,start_time,end_time,min):
    dataframe = dataframe.copy()
    
    # Convert the 'date' and 'start_time' columns to datetime objects
    dataframe['end_time'] = pd.to_datetime(dataframe['end_time'])
    # Set the start and end times for the time window
    start_time = pd.to_datetime(start_time).time()
    end_time = pd.to_datetime(end_time).time()

    # Create a list to store the data for the new dataframe
    data = []

    # Iterate over the unique dates in the 'date' column
    for date in dataframe['date'].unique():
        # Filter the rows for the current date
        df_date = dataframe[dataframe['date'] == date]
        df_date.loc[:, 'end_time'] = df_date['end_time'].dt.time  # Use .loc to modify the original DataFrame
        date = date + pd.Timedelta(minutes=min)
        # Create a time range for the current date with the specified time step
        time_range = pd.date_range(date, date + pd.Timedelta(days=1), freq=f'{time_step}T')

        # Iterate over the time range
        for start, end in zip(time_range[:-1], time_range[1:]):
            # Check if the start time is within the specified time window
            if start.time() >= start_time and start.time() < end_time:
                # Filter the rows for the current time window
                mask = (df_date['end_time'] >= start.time()) & (df_date['end_time'] < end.time())
                df_time_window = df_date[mask]
                # Calculate the average run time for each segment in the current time window
                avg_run_time = df_time_window.groupby('segment')['run_time_in_seconds'].mean().reset_index()

                # Append the data to the data list
                for row in avg_run_time.itertuples():
                    data.append((date, start.time(), row.segment, row.run_time_in_seconds))

    # Create a new dataframe from the data list
    df_avg_run_time = pd.DataFrame(data, columns=['date', 'start_time', 'segment', 'avg_run_time'])
    return df_avg_run_time

def fillTimeSteps(df_avg_run_time, startTime, endTime, time_step, num_segments):
    start_Time = pd.to_datetime(startTime).time()

    end_Time = pd.to_datetime(endTime).time()
    # Create a new DataFrame to store the missing data
    data = []

    # Iterate over the unique dates in the 'date' column
    for date in df_avg_run_time['date'].unique():
        # Filter the rows for the current date
        df_date = df_avg_run_time[df_avg_run_time['date'] == date]

        # Create a time range for the current date with the specified time step
        time_range = pd.date_range(date, date + pd.Timedelta(days=1), freq=f'{time_step}T').time

        # Iterate over the time range
        for t in time_range:
            # Check if the start time is within the specified time window
            if start_Time <= t < end_Time:
                # Check if the current start time is present in the dataframe
                if not (df_date['start_time'] == t).any():
                    # Add rows for the missing start time and segments
                    for segment in range(1, num_segments + 1):
                        data.append((date, t, segment, 0))

    # Create a new DataFrame from the data list
    df_missing = pd.DataFrame(data, columns=['date', 'start_time', 'segment', 'avg_run_time'])

    # Concatenate the new DataFrame with the original DataFrame
    df_avg_run_time = pd.concat([df_avg_run_time, df_missing], ignore_index=True)
    # Sort the rows of the dataframe by the 'date', 'start_time', and 'segment' columns
    df_avg_run_time = df_avg_run_time.sort_values(by=['date', 'start_time', 'segment'])
    return df_avg_run_time

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

# obtaining dataframe with average run times for each time and segment
df_avg_run_time = getAvgRuntimeWithSegment(busses_train,time_step,start_time,end_time,min)

# Create a MultiIndex with all combinations of date, start_time, and segment
idx = pd.MultiIndex.from_product([df_avg_run_time['date'].unique(), df_avg_run_time['start_time'].unique(), range(1, segments + 1)],
                                  names=['date', 'start_time', 'segment'])

# Reindex the dataframe using the new MultiIndex
df = df_avg_run_time.set_index(['date', 'start_time', 'segment']).reindex(idx, fill_value=0).reset_index()

df = fillTimeSteps(df, start_time, end_time, time_step, segments)

# Pivot the DataFrame
pivoted_df = df.pivot_table(index=['date', 'start_time'], columns='segment', values='avg_run_time', aggfunc='first')

avg_run_df = pivoted_df.reset_index()
avg_run_df['date'] = avg_run_df.apply(lambda x: pd.datetime.combine(x['date'], x['start_time']), axis=1)
avg_run_df = avg_run_df.drop("start_time",axis=1)

# file location to save Dataset
filename = 'avg_run_dir' + str(direction) + '.csv'
processed_data_file = os.path.join(dataSet_location, filename)

avg_run_df.to_csv(processed_data_file,index=False)

# Get the list of integer column names (segments)
segment_columns = pivoted_df.columns

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Loop through each segment column and normalize it
for segment in segment_columns:
    pivoted_df[segment] = scaler.fit_transform(pivoted_df[segment].values.reshape(-1, 1))

pivoted_df = pivoted_df.reset_index()
pivoted_df['date'] = pivoted_df.apply(lambda x: pd.datetime.combine(x['date'], x['start_time']), axis=1)
pivoted_df = pivoted_df.drop("start_time",axis=1)

def handlingZeros(df):
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.dayofweek
    df['time'] = df['date'].dt.time

    # Loop over each segment column
    for col in df.columns[1:-2]:
        # Group by weekday and time slot
        grouped = df.groupby(['weekday', 'time'])

        # Define a function to apply to each group
        def replace_zeros(group):
            nonzero_mean = group[group != 0].mean()
            if pd.notnull(nonzero_mean):
                return group.replace(0, nonzero_mean)
            else:
                return group

        # Apply the function to each group in the specific segment column
        df[col] = grouped[col].transform(replace_zeros)

    return df

def handlingOutliers(df, stdev_num):
    # Assuming 'df' is your DataFrame
    for col in df.columns:
        if np.issubdtype(df[col].dtype, np.number):  # check if column is numeric
            mean = df[col].mean()
            std = df[col].std()
            median = df[col].median()
            outliers = (df[col] - mean).abs() > stdev_num*std
            df.loc[outliers, col] = median
    return df

processed_df = handlingZeros(pivoted_df)
processed_df = handlingOutliers(processed_df,3)

# file location of the Saved Dataset
filename2 = 'processed_running_dir' + str(direction) + '.csv'
processed_data_file = os.path.join(dataSet_location, filename2)

processed_df.to_csv(processed_data_file,index=False)