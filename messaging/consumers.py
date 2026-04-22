import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.get_or_create_room(self.room_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        user = self.scope['user']

        if user.is_anonymous:
            return

        await self.save_message(user, self.room_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message'],
        }))

    @database_sync_to_async
    def get_or_create_room(self, room_name):
        ChatRoom.objects.get_or_create(name=room_name)

    @database_sync_to_async
    def save_message(self, user, room_name, content):
        room, _ = ChatRoom.objects.get_or_create(name=room_name)
        Message.objects.create(room=room, sender=user, content=content)
