from insert_runtime import addRunningTime
from insert_stop_time import addStopTime


def addData(startTime, endTime):
    addStopTime(startTime, endTime)
    addRunningTime(startTime, endTime)
