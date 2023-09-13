from django.core.management.base import BaseCommand
import time

import os
import sys

# Add the path to the directory containing getArrivalTimes.py
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(rootPath)

from timer import timer

class Command(BaseCommand):
    help = 'Run a background script'

    def handle(self, *args, **options):
        # Your background script code here
        timer()
        # while True:
        #     self.stdout.write(self.style.SUCCESS('Running in the background...'))
        #     time.sleep(10)  # Adjust the sleep interval as needed
