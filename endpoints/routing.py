from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/esp/<room_id>/', consumers.ClinicConsumer.as_asgi()),
]
