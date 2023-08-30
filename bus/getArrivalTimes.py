from datetime import datetime, timedelta
from keras.models import load_model
from get_runtime_pred import getRunTimePrediction
from get_dwelltime_pred import getDwellTimePrediction

import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus.settings')
application = get_wsgi_application()


segments = 14
segments_up = 114
segments_down = 101

import numpy as np
from bus.models import BusRunningPredictions,BusDwellTimePredictions

def getRunPred():
    # Query the BusRunningPredictions table
    queryset = BusRunningPredictions.objects.all()

    # Extract the data from the queryset
    data = []
    for obj in queryset:
        row = [
            obj.segment_1,
            obj.segment_2,
            obj.segment_3,
            obj.segment_4,
            obj.segment_5,
            obj.segment_6,
            obj.segment_7,
            obj.segment_8,
            obj.segment_9,
            obj.segment_10,
            obj.segment_11,
            obj.segment_12,
            obj.segment_13,
            obj.segment_14,
            obj.segment_15
        ]
        data.append(row)

    # Convert the data to a numpy array
    data = np.array(data)

    # Reshape the data to have shape (5, 15, 1, 1)
    data = data.reshape((5, 15, 1, 1))

    return data


def getDwellPred():
    # Query the BusRunningPredictions table
    queryset = BusRunningPredictions.objects.all()

    # Extract the data from the queryset
    data = []
    for obj in queryset:
        row = [
            obj.stop_101,
            obj.stop_102,
            obj.stop_103,
            obj.stop_104,
            obj.stop_105,
            obj.stop_106,
            obj.stop_107,
            obj.stop_108,
            obj.stop_109,
            obj.stop_100,
            obj.stop_111,
            obj.stop_112,
            obj.stop_113,
            obj.stop_114,
        ]
        data.append(row)

    # Convert the data to a numpy array
    data = np.array(data)

    # Reshape the data to have shape (5, 15, 1, 1)
    data = data.reshape((5, 14, 1, 1))

    return data

def time_in_new_step(time_str, seconds_to_add):
    # Convert input time string to datetime object
    input_time = datetime.strptime(time_str, '%H:%M:%S')

    # Convert seconds_to_add to an integer
    seconds_to_add = int(seconds_to_add)

    # Calculate the new time after adding seconds
    new_time = input_time + timedelta(seconds=seconds_to_add)

    # Calculate the current and new time steps (15-minute intervals)
    current_time_step = (input_time.minute // 15) + 1
    new_time_step = (new_time.minute // 15) + 1

    # Check if the time step changed
    step_changed = current_time_step != new_time_step

    return new_time.strftime('%H:%M:%S'), step_changed


def getArrivalTimes(current_time,next_stop):

    d = getDwellPred()
    r = getRunPred()

    t = '06:39:49'
    stop = 101

    start_datetime = "2021-10-01 06:00:00"
    end_datetime = "2021-10-01 14:00:00"



    for i in range(segments):
        stops = {x: 0 for x in range(stop + i, segments_up + 1)}
        times = {x: 0 for x in range(stop + i, segments_up + 1)}
        k = 0
        dwell = 0
        dwell_prev = 0
        run = 0
        for j in range(stop + i, segments_up + 1):
            if j == stop:
                run = r[k][j - segments_down][0][0]
                stops[j] = run
                # print(stops[j],j-segments_down)
            else:
                runs = [r[k][j - segments_down][0][0]]
                for i in range(1, 4):
                    if k + i > 4:
                        break
                    runs.append(r[k + i][j - segments_down][0][0])
                run = max(runs)

                dwells = [d[k][j - segments_down - 1][0][0]]
                for i in range(1, 4):
                    if k + i > 4:
                        break
                    dwells.append(d[k + i][j - segments_down - 1][0][0])
                dwell = max(dwells)

                stops[j] = run + dwell + stops[j - 1]
                # print(run,dwell)
            # print(run,dwell,dwell_prev)
            new_time, step_changed = time_in_new_step(t, run + dwell + dwell_prev)
            times[j] = new_time
            dwell_prev = dwell
            t = new_time
            if step_changed:
                # print(new_time, k)
                k += 1
                if k > 4:
                    break
        return times
