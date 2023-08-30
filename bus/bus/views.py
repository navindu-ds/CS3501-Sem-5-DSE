from django.http import JsonResponse
# Now you can import your module from the parent directory

import sys
import os

# Add the path to the directory containing getArrivalTimes.py
getArrivalTimes_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(getArrivalTimes_dir)

# Now you can import getArrivalTimes
from getArrivalTimes import getArrivalTimes
from getAllArrivals import getAllArrivals

# Rest of your views.py code

def arrivals(request):
    data = getAllArrivals()
    return JsonResponse(data, safe=False)