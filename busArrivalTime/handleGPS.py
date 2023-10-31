import random
import pandas as pd
from databaseDetails import database
import mysql.connector

def getGPSData(bus, time):
    # print(bus, time)
    # Database connection parameters (modify these with your actual values)
    config = database

    # Establish a connection to the database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Your SQL query
    query = """
    SELECT *
    FROM gps_points
    WHERE deviceid = %s
    AND devicetime BETWEEN %s AND DATE_ADD(%s, INTERVAL 5 MINUTE) 
    AND latitude != 0 and longitude != 0
    ORDER BY devicetime ASC
    LIMIT 1;
    """

    # Execute the query
    cursor.execute(query, (bus, time, time))

    # Fetch the result
    result = cursor.fetchone()
    # print(result)
    # Close the cursor and connection
    cursor.close()
    cnx.close()

    if result:
        lat = result[3]  # Assuming latitude is the 4th column in your result
        lon = result[4]  # Assuming longitude is the 5th column in your result
        return (lat, lon)
    else:
        return (0, 0)  # Return None values if no result is found



def getLocations():
    dataset = pd.read_csv('data/busses_train.csv')
    return dataset