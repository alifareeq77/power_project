import json
import logging
import aioredis
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from endpoints.models import Esp

logger = logging.getLogger(__name__)


class ClinicConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def get_esp_statue(self, token):
        data = Esp.objects.filter(token=token).first().give_esp_statue(token)
        return data

    @database_sync_to_async
    def get_esp_statuee(self, id_n):
        data = Esp.objects.filter(id=id_n).first()
        data = {'statue': data.status}
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
        await self.channel_layer.group_send(
            self.token_group, await self.get_esp_statue(self.token)
        )

    async def disconnect(self, close_code):
        # Leave room group
        if not self.scope["user"].is_anonymous:
            await self.channel_layer.group_send(
                self.token_group, {
                    "type": 'disconnecting'})
            await self.channel_layer.group_discard(
                self.token_group,
                self.channel_name
            )

    async def statue_updated(self, event):
        await self.send_json(event)

    async def websocket_handshake(self, event):
        await self.send_json(event)

    async def disconnecting(self, event):
        await self.send_json(event)

    async def current_statue(self, event):
        await self.send_json(event)
