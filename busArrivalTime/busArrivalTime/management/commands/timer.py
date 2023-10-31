from django.core.management.base import BaseCommand
import time

import os
import sys

# Add the path to the directory containing getArrivalTimes.py
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(rootPath)

from timer import timer
from models import load_run_model, load_dwell_model


class Command(BaseCommand):
    help = 'Run a background script'

    def handle(self, *args, **options):
        # Your background script code here
        runModel = load_run_model()
        dwellModel = load_dwell_model()
        timer(runModel,dwellModel)
        # while True:
        #     self.stdout.write(self.style.SUCCESS('Running in the background...'))
        #     time.sleep(10)  # Adjust the sleep interval as needed