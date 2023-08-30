import mysql.connector
import pandas as pd
import numpy as np

def handleOutliers(df):
    # Calculate the median of avg_run_time
    median_avg_run_time = df['avg_run_time'].median()

    # Calculate the absolute deviations
    df['abs_deviation'] = np.abs(df['avg_run_time'] - median_avg_run_time)

    # Calculate the median absolute deviation (MAD)
    mad = df['abs_deviation'].median()

    # Set a threshold (for example, 3 times MAD) to identify outliers
    threshold = 3 * mad

    # Replace outliers with the median value
    df.loc[df['abs_deviation'] > threshold, 'avg_run_time'] = median_avg_run_time

    # Drop the temporary column
    df = df.drop(columns=['abs_deviation'])

    return df

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "ch1965298th",
    "database": "bus",
}

def getDwellTimePrediction(model,start_datetime,end_datetime):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Specify the start datetime and end datetime
    # start_datetime = "2021-10-01 06:00:00"
    # end_datetime = "2021-10-01 14:00:00"

    query = """
        SELECT *
        FROM bus_stop_times
        WHERE CONCAT(date, ' ', arrival_time) BETWEEN %s AND %s
    """
    params = (start_datetime, end_datetime)
    cursor.execute(query, params)

    results = cursor.fetchall()

    # Your retrieved rows
    retrieved_rows = []

    for row in results:
        row = list(row)
        retrieved_rows.append(row)

    # Create a DataFrame from the retrieved rows
    columns = [
        "id", "trip_id", "deviceid", "direction", "bus_stop", "date", "arrival_time", "departure_time", 'dwell_time',
        "dwell_time_in_seconds_old", "day_of_week", "time_of_day",
        "Sunday/holiday", "saturday", "weekday/end", "week_no", "rt(w-1)", "rt(w-2)",
        "rt(w-3)", "rt(t-1)", "rt(t-2)", "rt(n-1)", "rt(n-2)", "rt(n-3)", "hour_of_day",
        "day", "month", "temp", "precip", "windspeed", "conditions", "dt(n-1)", 'p', 'q'
    ]

    # Create the DataFrame
    initial = pd.DataFrame(retrieved_rows, columns=columns)

    initial.rename(columns={'bus_stop': 'segment'}, inplace=True)
    initial.rename(columns={'arrival_time': 'start_time'}, inplace=True)
    initial.rename(columns={'departure_time': 'end_time'}, inplace=True)
    initial.rename(columns={'dwell_time': 'run_time'}, inplace=True)
    initial.rename(columns={'dwell_time_in_seconds_old': 'run_time_in_seconds'}, inplace=True)

    busses_new = initial[['trip_id', 'deviceid', 'direction', 'segment', 'date', 'start_time', 'end_time', 'run_time',
                          'run_time_in_seconds']]

    busses_new.dropna(inplace=True)

    segments_up = 114
    segments_down = 101
    segments = 14
    time_step = 15
    w = 52
    pred_steps = 5
    start_time = start_datetime
    end_time = end_datetime

    mask = (segments_down <= busses_new['segment']) & (busses_new['segment'] <= segments_up)

    busses_new = busses_new[mask]

    # Convert the 'date' column to a datetime object
    busses_new['date'] = pd.to_datetime(busses_new['date'])

    # Create the train and test dataframes
    busses_train = busses_new

    # Assuming `busses_train` is the input dataframe
    df = busses_train.copy()
    df['start_time'] = df['start_time'].astype(str)
    df['end_time'] = df['end_time'].astype(str)
    df['date'] = df['date'].astype(str)
    df['start_time'] = df['start_time'].apply(lambda x: x[-8:])
    df['end_time'] = df['end_time'].apply(lambda x: x[-8:])
    # Assuming that your DataFrame is stored in a variable named df
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['start_time'])

    # Convert start_time and end_time to datetime
    df['start_time'] = pd.to_datetime(df['start_time'], format='%H:%M:%S').dt.time
    df['end_time'] = pd.to_datetime(df['end_time'], format='%H:%M:%S').dt.time

    # Round start_time down to nearest 15 minutes
    df['start_time'] = df['start_time'].apply(
        lambda dt: dt.replace(minute=0, second=0) if dt.minute < 15 else dt.replace(minute=15,
                                                                                    second=0) if dt.minute < 30 else dt.replace(
            minute=30, second=0) if dt.minute < 45 else dt.replace(minute=45, second=0))

    # Filter rows based on start and end datetime
    start_datetime = pd.to_datetime(start_datetime)
    end_datetime = pd.to_datetime(end_datetime)
    df = df[(df['datetime'] >= start_datetime) & (df['datetime'] <= end_datetime)]

    # Group by date, start_time and segment, and calculate average run time
    result = df.groupby(['date', 'start_time', 'segment'])['run_time_in_seconds'].mean().reset_index()

    # Rename columns
    result.columns = ['date', 'start_time', 'segment', 'avg_run_time']

    df = handleOutliers(result)

    # Create a MultiIndex with all combinations of date, start_time, and segment
    idx = pd.MultiIndex.from_product(
        [df['date'].unique(), df['start_time'].unique(), range(segments_down, segments_up + 1)],
        names=['date', 'start_time', 'segment'])

    # Reindex the dataframe using the new MultiIndex
    df = df.set_index(['date', 'start_time', 'segment']).reindex(idx, fill_value=0).reset_index()

    # Assuming `result` is the resulting dataframe from the previous code snippet
    result = df.copy()

    # Create a new dataframe with all possible combinations of date, start_time and segment
    dates = result['date'].unique()
    end_datetime = end_datetime - pd.Timedelta(minutes=15)
    start_times = pd.date_range(start_datetime, end_datetime, freq='15min').time
    segments = result['segment'].unique()
    all_combinations = pd.MultiIndex.from_product([dates, start_times, segments],
                                                  names=['date', 'start_time', 'segment']).to_frame(index=False)

    # Merge result with all_combinations and fill missing values with 0
    result = pd.merge(all_combinations, result, on=['date', 'start_time', 'segment'], how='left').fillna(0)

    df = result.copy()

    # Pivot the DataFrame
    pivoted_df = df.pivot_table(index=['date', 'start_time'], columns='segment', values='avg_run_time', aggfunc='first')

    # define the min and max values for each column
    min_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    max_values = [457, 420, 403, 300, 540, 420, 300, 97, 540, 420, 300, 300, 420, 300]

    # apply min-max scaling to each column
    for i in range(segments_down, segments_up + 1):
        pivoted_df[i] = (pivoted_df[i] - min_values[i - segments_down]) / (
                    max_values[i - segments_down] - min_values[i - segments_down])

    columns = len(pivoted_df.columns)
    sequences = [np.array(pivoted_df[[i]]) for i in range(segments_down, segments_up + 1)]

    sequence_length_x = 32

    future_steps = 5

    arrangement_x = np.array([[[sequences[k][i + j] for k in range(columns)]
                               for j in range(sequence_length_x)] for i in
                              range(len(sequences[0]) - sequence_length_x + 1)])

    X0 = arrangement_x.reshape((len(arrangement_x), sequence_length_x, columns, 1, 1))

    # from keras.models import load_model

    # load the saved model
    # model = load_model('ConvLSTM_dwell_time.h5')

    predictions = model.predict(X0)

    for i in range(14):
        for j in range(5):
            predictions[0][j][i][0][0] = predictions[0][j][i][0][0] * max_values[i]


    cursor.close()
    conn.close()

    return predictions[0]

