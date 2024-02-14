"""
ASGI config for driver_tracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "driver_tracker.settings")

application = get_asgi_application()


# its important to make all other imports below this comment
import socketio
from map.Simulation import *

application = socketio.ASGIApp(sio, application)