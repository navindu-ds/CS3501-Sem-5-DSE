from django.core import serializers
from django.http import JsonResponse
from .models import ArrivalTimes
from django.db import connection

def get_avg_buses(request):
    # Assuming you get the current date and time from the `date_and_time` table
    try:
        with connection.cursor() as cursor:
            print('dddddd')
            # Get the current date and time from the `date_and_time` table
            cursor.execute("SELECT date, time FROM date_and_time WHERE id >= 1")  # Assuming you have a specific row in the table
            print('kokokoko')
            date, time = cursor.fetchone()
            print(date, time,'aaaaaa')
            # Get the day of the week (0-6) from the current date
            day_of_week = date.weekday()

            # Get the hour (4-23) from the current time
            hour = time.hour
            # Construct the SQL query to fetch the value
            sql_query = f"""
            SELECT hour_{hour}
            FROM avg_buses
            WHERE day_of_week = {day_of_week}
            """

            cursor.execute(sql_query)
            result = cursor.fetchone()

            if result is not None:
                avg_bus_value = result[0]
                response_data = {
                    'day_of_week': day_of_week,
                    'hour': hour,
                    'time': time,
                    'date': date,
                    'avg_bus_value': avg_bus_value,
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'No data found for the given day and hour'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_arrival_times(request):
    data = serializers.serialize('json', ArrivalTimes.objects.all())
    return JsonResponse(data, safe=False)
