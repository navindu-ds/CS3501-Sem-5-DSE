import mysql.connector
from databaseDetails import database
def updateTime(time,date):
    # Establish a connection to the MySQL server
    conn = mysql.connector.connect(**database)

    # Create a cursor object to execute queries
    cursor = conn.cursor()

    # Define the date and time values
    date = date
    time = time

    # Clear the table
    cursor.execute("DELETE FROM date_and_time")

    # Insert the new values into the table
    cursor.execute(f"INSERT INTO date_and_time (date, time) VALUES ('{date}', '{time}')")

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
