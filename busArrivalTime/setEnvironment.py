import os

def getApplication():
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ['DJANGO_SETTINGS_MODULE'] = 'busArrivalTime.settings'

    # Now you can set up the Django environment
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    return application