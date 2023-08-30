import os
import numpy as np
from django.core.wsgi import get_wsgi_application
from get_runtime_pred import getRunTimePrediction
from get_dwelltime_pred import getDwellTimePrediction

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus.settings')
application = get_wsgi_application()

from bus.models import BusRunningPredictions,BusDwellTimePredictions


def addRunTimePrediction(model, start_datetime, end_datetime):
    # assuming you have a numpy array named 'data' with shape (5, 15, 1, 1)
    data = getRunTimePrediction(model, start_datetime, end_datetime)

    # iterate over the rows of the data array
    for row in data:
        # create a new BusRunningPredictions object
        prediction = BusRunningPredictions(
            segment_1=row[0][0][0],
            segment_2=row[1][0][0],
            segment_3=row[2][0][0],
            segment_4=row[3][0][0],
            segment_5=row[4][0][0],
            segment_6=row[5][0][0],
            segment_7=row[6][0][0],
            segment_8=row[7][0][0],
            segment_9=row[8][0][0],
            segment_10=row[9][0][0],
            segment_11=row[10][0][0],
            segment_12=row[11][0][0],
            segment_13=row[12][0][0],
            segment_14=row[13][0][0],
            segment_15=row[14][0][0]
        )

        # save the new object to the database
        prediction.save()


def addDwellTimePrediction(model, start_datetime, end_datetime):
    data = getDwellTimePrediction(model, start_datetime, end_datetime)

    # iterate over the rows of the data array
    for row in data:
        # create a new BusRunningPredictions object
        prediction = BusDwellTimePredictions(
            stop_101=row[0][0][0],
            stop_102=row[1][0][0],
            stop_103=row[2][0][0],
            stop_104=row[3][0][0],
            stop_105=row[4][0][0],
            stop_106=row[5][0][0],
            stop_107=row[6][0][0],
            stop_108=row[7][0][0],
            stop_109=row[8][0][0],
            stop_110=row[9][0][0],
            stop_111=row[10][0][0],
            stop_112=row[11][0][0],
            stop_113=row[12][0][0],
            stop_114=row[13][0][0],
        )

        # save the new object to the database
        prediction.save()
