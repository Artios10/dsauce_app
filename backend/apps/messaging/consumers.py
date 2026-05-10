import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.messaging.models import Conversation, Message
from apps.notifications.services import create_notification


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = str(self.scope['url_route']['kwargs']['conversation_id'])
        self.room_group_name = f'chat_{self.conversation_id}'

        if not await self._is_participant(self.scope['user'].id, self.conversation_id):
            await self.close(code=4001)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        payload = json.loads(text_data)
        action = payload.get('action')

        if action == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_event',
                    'user_id': self.scope['user'].id,
                    'is_typing': payload.get('is_typing', False),
                },
            )
        elif action == 'message':
            message = await self._create_message(payload.get('content', ''))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_event',
                    'message': message,
                },
            )

    async def typing_event(self, event):
        await self.send(text_data=json.dumps({'event': 'typing', **event}))

    async def message_event(self, event):
        await self.send(text_data=json.dumps({'event': 'message', **event}))

    @database_sync_to_async
    def _is_participant(self, user_id, conversation_id):
        return Conversation.objects.filter(id=conversation_id, participants__id=user_id).exists()

    @database_sync_to_async
    def _create_message(self, content):
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(conversation=conversation, sender=self.scope['user'], content=content)
        for participant in conversation.participants.exclude(id=self.scope['user'].id):
            create_notification(
                recipient=participant,
                actor=self.scope['user'],
                notification_type='message',
                title='New message',
                message=f'New message from {self.scope["user"].username}',
                metadata={'conversation_id': str(conversation.id), 'message_id': message.id},
            )
        return {
            'id': message.id,
            'conversation': str(conversation.id),
            'sender': self.scope['user'].id,
            'sender_username': self.scope['user'].username,
            'content': message.content,
            'created_at': message.created_at.isoformat(),
        }


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close(code=4001)
            return
        self.group_name = 'presence'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'presence_event', 'user_id': self.scope['user'].id, 'status': 'online'},
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'presence_event', 'user_id': self.scope['user'].id, 'status': 'offline'},
        )

    async def presence_event(self, event):
        await self.send(text_data=json.dumps({'event': 'presence', **event}))
