import asyncio
import json
from logging import getLogger

from channels.generic.websocket import AsyncWebsocketConsumer

from common.custom_authentications import authenticate
from common.socket_serializer import serialize_json

logger = getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await authenticate(self)
        self.ping_task = asyncio.create_task(self.send_periodic_ping())

    async def send_periodic_ping(self):
        try:
            while True:
                await asyncio.sleep(15)
                await self.send_json({"type": "ping"})
                logger.info("Ping sent to client")
        except asyncio.CancelledError:
            pass

    async def receive_json(self, content):
        if content.get("type") == "pong":
            logger.info("Pong received from client")
            pass

    async def receive(self, text_data):
        await serialize_json(self, text_data)

    async def notification(self, event):
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, close_code):
        if hasattr(self, "ping_task"):
            self.ping_task.cancel()
            logger.info("Ping task cancelled")
