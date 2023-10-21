import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

import warnings
warnings.filterwarnings("ignore")

from sklearn.preprocessing import MinMaxScaler

current_folder = (os.path.abspath(''))
dataSet_location = os.path.join(current_folder,'Datasets')
avgRunFile = os.path.join(dataSet_location,'avg_run_15min_dir1.csv')

# dataframe of average running times for each segement for each time slot in history
avg_run_df = pd.read_csv(avgRunFile)

# additional columns
avg_run_df['date'] = pd.to_datetime(avg_run_df['date'])
avg_run_df['weekday'] = avg_run_df['date'].dt.dayofweek
avg_run_df['time'] = avg_run_df['date'].dt.time

def handlingZeros(df):
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

processed_df = handlingZeros(avg_run_df)
processed_df = handlingOutliers(processed_df,3)

# Get the list of integer column names (segments)
segment_columns = processed_df.columns[1:-2]

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Loop through each segment column and normalize it
for segment in segment_columns:
    processed_df[segment] = scaler.fit_transform(processed_df[segment].values.reshape(-1, 1))

print(processed_df)