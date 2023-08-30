from datetime import datetime, timedelta
from keras.models import load_model
from get_runtime_pred import getRunTimePrediction
from get_dwelltime_pred import getDwellTimePrediction

segments = 14
segments_up = 114
segments_down = 101


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



t = '06:39:49'
stop = 101

model_dwell = load_model('ConvLSTM_dwell_time.h5')
model_run = load_model('ConvLSTM_runTime.h5')

start_datetime = "2021-10-01 06:00:00"
end_datetime = "2021-10-01 14:00:00"

r = getRunTimePrediction(model_run, start_datetime, end_datetime)
d = getDwellTimePrediction(model_dwell, start_datetime, end_datetime)


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
    print(stops)
    print(times)
    break
