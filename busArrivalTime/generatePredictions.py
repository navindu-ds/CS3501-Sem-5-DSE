from datetime import datetime, timedelta
from routeDetails import *
from databaseDetails import database
import torch
import numpy as np
import mysql.connector
import pandas as pd
from models import device


def fetch_dwelltimes(input_datetime: str) -> pd.DataFrame:
    # Database connection details
    config = {**database, 'raise_on_warnings': True}

    # Connect to the MySQL database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Set input_datetime variable in SQL
    cursor.execute(f"SET @input_datetime = '{input_datetime}';")
    cursor.execute(
        "SET @matched_datetime = (SELECT datetime FROM avg_dwell_time WHERE datetime = @input_datetime LIMIT 1);")
    cursor.execute(
        "SET @matched_datetime = COALESCE(@matched_datetime, (SELECT MAX(datetime) FROM avg_dwell_time WHERE datetime <= @input_datetime AND @input_datetime <= DATE_ADD(datetime, INTERVAL 5 MINUTE)));")

    # Execute the SELECT statement
    cursor.execute("""
        SELECT * 
        FROM avg_dwell_time
        WHERE datetime < @matched_datetime
        ORDER BY datetime desc
        LIMIT 96;
    """)

    # Fetch the results
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    # Convert results to pandas DataFrame
    df = pd.DataFrame(rows, columns=column_names)

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return df


def fetch_runtimes(input_datetime: str) -> pd.DataFrame:
    # Database connection details
    config = {**database, 'raise_on_warnings': True}

    # Connect to the MySQL database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Set input_datetime variable in SQL
    cursor.execute(f"SET @input_datetime = '{input_datetime}';")
    cursor.execute(
        "SET @matched_datetime = (SELECT datetime FROM avg_run_time WHERE datetime = @input_datetime LIMIT 1);")
    cursor.execute(
        "SET @matched_datetime = COALESCE(@matched_datetime, (SELECT MAX(datetime) FROM avg_run_time WHERE datetime <= @input_datetime AND @input_datetime <= DATE_ADD(datetime, INTERVAL 5 MINUTE)));")

    # Execute the SELECT statement
    cursor.execute("""
        SELECT * 
        FROM avg_run_time
        WHERE datetime < @matched_datetime
        ORDER BY datetime desc
        LIMIT 96;
    """)

    # Fetch the results
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    # Convert results to pandas DataFrame
    df = pd.DataFrame(rows, columns=column_names)

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return df


runScalingParams = {'1': {'min': 0.0, 'max': 900.0},
                    '2': {'min': 0.0, 'max': 1005.0},
                    '3': {'min': 0.0, 'max': 1199.0},
                    '4': {'min': 0.0, 'max': 971.0},
                    '5': {'min': 0.0, 'max': 879.0},
                    '6': {'min': 0.0, 'max': 743.0},
                    '7': {'min': 0.0, 'max': 529.0},
                    '8': {'min': 0.0, 'max': 304.0},
                    '9': {'min': 0.0, 'max': 249.0},
                    '10': {'min': 0.0, 'max': 859.0},
                    '11': {'min': 0.0, 'max': 808.0},
                    '12': {'min': 0.0, 'max': 900.0},
                    '13': {'min': 0.0, 'max': 788.0},
                    '14': {'min': 0.0, 'max': 900.0},
                    '15': {'min': 0.0, 'max': 1118.0}}

dwellScalingParams = {'101': {'min': 0.0, 'max': 81.77777777777777},
                      '102': {'min': 0.0, 'max': 82.72222222222223},
                      '103': {'min': 8.509876543209874, 'max': 49.48201058201058},
                      '104': {'min': 1.861111111111108, 'max': 43.81018518518518},
                      '105': {'min': 15.689814814814829, 'max': 238.84201940035277},
                      '106': {'min': 10.90352733686067, 'max': 76.21276455026455},
                      '107': {'min': 7.555555555555555, 'max': 52.58756613756614},
                      '108': {'min': 10.045767195767196, 'max': 29.775694444444444},
                      '109': {'min': 15.573412698412685, 'max': 168.9973544973545},
                      '110': {'min': 10.181790123456791, 'max': 89.8721961680295},
                      '111': {'min': 2.7407407407407374, 'max': 59.716880110630115},
                      '112': {'min': 2.9722222222222223, 'max': 31.75548941798942},
                      '113': {'min': 4.486111111111118, 'max': 178.0579805996473},
                      '114': {'min': 7.055555555555555, 'max': 43.478439153439155}}


def get_torch_tensor(df, device):
    return torch.tensor(df, dtype=torch.float32).to(device)


def getSamplePrediction(df, model, scaling_params1, segments=15, steps=5, k=0):
    sorted_df = df.sort_values(by='datetime', ascending=True)
    sorted_df = sorted_df.drop(columns=['datetime'])
    dval = sorted_df.values
    X3 = np.array([[dval]])
    X_tensor = get_torch_tensor(X3, device)
    model.eval()
    with torch.no_grad():
        predictions = model(X_tensor)
    predictions_numpy = np.array([tensor.cpu().numpy() for tensor in predictions])
    predictions_numpy = predictions_numpy.reshape((steps, segments))
    pred1 = []
    for j in range(5):
        inverse_scaled_array = np.array([predictions_numpy[j][i] * (
                    scaling_params1[str(i + 1 + k)]['max'] - scaling_params1[str(i + 1 + k)]['min']) +
                                         scaling_params1[str(i + 1 + k)]['min'] for i in
                                         range(len(predictions_numpy[j]))])
        pred1.append(inverse_scaled_array)
    final = np.array(pred1)
    return final


def getNextFive(curr):
    # Extract the minute
    current_minute = curr.minute

    # Determine how many minutes to add to reach the next multiple of 5
    minutes_to_add = 5 - (current_minute % 5)

    # Add the required minutes
    next_time_dt = curr + timedelta(minutes=minutes_to_add)

    # Extract the time part
    next_time_obj = next_time_dt.time()

    return next_time_obj


def generatePredictions(segment, start_time, run, dwell):
    # Check if start_time is a string
    if isinstance(start_time, str):
        # Convert start_time to datetime object
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    temp = start_time.strftime('%Y-%m-%d %H:%M:%S')
    dfRun = fetch_runtimes(temp)
    dfDwell = fetch_dwelltimes(temp)
    predRun = getSamplePrediction(dfRun, run, runScalingParams)
    predDwell = getSamplePrediction(dfDwell, dwell, dwellScalingParams, segments=14, k=100)
    # print(predRun)
    # start_time += timedelta(minutes=5)
    # Initialize the dictionary with the first segment and start_time
    arrivalTimes = dict()

    for seg in busStops[:int(segment) - 1]:
        # Add new segment and time to dictionary
        arrivalTimes[seg] = 'passed'

    current_time_dt = start_time
    next = getNextFive(current_time_dt)
    current_time_dt += timedelta(seconds=float(predRun[0][int(segment) - 1]))
    # print(current_time_dt)
    arrivalTimes[str(int(segment) + 100)] = current_time_dt.strftime('%H:%M:%S')
    if segment == 15:
        return arrivalTimes
    segment += 1
    i = 0
    if current_time_dt.time() >= next:
        i += 1
        next = getNextFive(current_time_dt)
    while segment <= 15 and i <= 4:
        dt = float(predDwell[i][int(segment) - 2])
        current_time_dt += timedelta(seconds=dt)
        if current_time_dt.time() >= next:
            i += 1
            next = getNextFive(current_time_dt)
        if i == 5:
            break
        rt = float(predRun[i][int(segment)-1])
        current_time_dt += timedelta(seconds=rt)
        # print(current_time_dt)
        arrivalTimes[str(int(segment) + 100)] = current_time_dt.strftime('%H:%M:%S')
        segment += 1

    # Generate the rest of the segments
    for seg in busStops[int(segment) - 1:]:
        # Add new segment and time to dictionary
        arrivalTimes[seg] = current_time_dt.strftime('%H:%M:%S')
        # Increase time by 1 minute
        current_time_dt += timedelta(seconds=71)
    print(arrivalTimes)
    return arrivalTimes