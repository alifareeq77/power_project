import json

import aioredis
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from endpoints.models import Esp


class ESP32WebsocketConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_esp_statue(self, token):
        data = Esp.objects.filter(token=token).first().give_esp_statue(token)
        return data

    async def connect(self):
        self.token = self.scope['url_route']['kwargs']['room_id']
        self.token_group = 'esp_%s' % self.token
        self.r_conn = await aioredis.create_redis(
            "redis://localhost"
        )
        await self.channel_layer.group_add(
            self.token_group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f'esp disconnected with st code :{close_code}')

    async def receive(self, text_data):
        print(f'Received message: {text_data}')

    async def send_response(self, response_data):
        await self.send(response_data)

    async def statue_updated(self, event):
        print(event)
        updated_fields = event['statue']
        await self.send(str(updated_fields))
