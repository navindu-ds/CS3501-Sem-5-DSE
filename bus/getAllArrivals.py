import mysql.connector
from datetime import datetime, timedelta

from getArrivalTimes import getArrivalTimes

import mysql.connector

def get_date_time():
    # Establish a connection to the MySQL server
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='ch1965298th',
        database='bus'
    )

    # Create a cursor object to execute queries
    cursor = conn.cursor()

    # Define the query
    query = "SELECT date, time FROM date_and_time LIMIT 1"

    # Execute the query
    cursor.execute(query)

    # Fetch the resulting row
    row = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Extract the date and time values from the row
    date, time = row

    # Convert the date and time values to strings
    date_str = date.strftime('%Y-%m-%d')
    time_str = str(time)

    # Return the date and time strings
    return date_str, time_str


def getAllArrivals():

    # Establish a connection to the MySQL server
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='ch1965298th',
        database='bus'
    )

    # Create a cursor object to execute queries
    cursor = conn.cursor()

    dt = get_date_time()

    date = dt[0]
    # Define the end time string
    end = dt[1]

    # Convert the end time string to a datetime object
    end_time = datetime.strptime(end, '%H:%M:%S')

    # Subtract one minute from the end time
    start_time = end_time - timedelta(minutes=1)

    # Convert the start time to a string
    start = start_time.strftime('%H:%M:%S')


    query1 = f"""
    select distinct deviceid
    from bus_running_times
    where date = '{date}' and start_time < '{end}' and start_time > '{start}'
    """



    # Execute the query
    cursor.execute(query1)

    # Fetch the resulting row
    results = cursor.fetchall()

    ids = []

    for row in results:
        # print(int(row[0]))
        ids.append(int(row[0]))

    busses = []

    for id in ids:
        # Define the query
        query2 = f"""
        SELECT deviceid,segment,date,start_time,end_time
        FROM bus_running_times
        WHERE deviceid = {id}
        AND start_time < '{end}'
        AND start_time > '{start}'
        AND date = '{date}'
        AND start_time = (
            SELECT MAX(start_time)
            FROM bus_running_times
            WHERE deviceid = {id}
            AND start_time < '{end}'
            AND start_time > '{start}'
            AND date = '{date}'
        )
        LIMIT 1;
        """
        cursor.execute(query2)

        # Fetch the resulting row
        result = cursor.fetchone()
        busses.append(result)

    # print(busses)

    # Convert end_time to seconds
    h, m, s = map(int, end.split(':'))
    end_time_seconds = h * 3600 + m * 60 + s

    segments = []

    # Check each item in the list
    for bus in busses:
        if bus[4].seconds > end_time_seconds:
            # print(bus[1] + 1)
            segments.append(int(bus[1] + 1))
        else:
            # print(bus[1] + 2)
            segments.append(int(bus[1] + 2))
    # print(segments)

    arrivals = [[segment,getArrivalTimes(end,segment+100)] for segment in segments]

    # print(arrivals)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return arrivals

# print(getAllArrivals())