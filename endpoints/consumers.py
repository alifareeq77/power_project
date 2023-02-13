import logging
import aioredis
from channels.generic.websocket import AsyncJsonWebsocketConsumer


logger = logging.getLogger(__name__)


class ClinicConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.token = self.scope['url_route']['kwargs']['room_id']
        print(self.token)
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
        # Leave room group
        if not self.scope["user"].is_anonymous:
            await self.channel_layer.group_send(
                self.token_group, {
                    "message": 'disconnecting'})
            await self.channel_layer.group_discard(
                self.token_group,
                self.channel_name
            )

    async def session_created(self, event):
        await self.send_json(event)

    async def session_updated(self, event):
        await self.send_json(event)

    async def session_join(self, event):
        await self.send_json(event)

    async def session_leave(self, event):
        await self.send_json(event)
