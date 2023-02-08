# Django Channels consumer

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class LEDControlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Send a message to the ESP32 to turn on the LED
        await self.send(text_data=json.dumps({
            'command': 'turn_on'
        }))
