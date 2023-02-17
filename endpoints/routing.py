from django.urls import re_path, path
from . import consumers, consy

websocket_urlpatterns = [
    path('ws/esp/<room_id>/', consumers.ClinicConsumer.as_asgi()),
    # path('ws/esp/<room_id>/', consy.ESP32WebsocketConsumer.as_asgi()),
    # path('ws/esp/test/', consumers.ClinicConsumer.as_asgi()),
]
