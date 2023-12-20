# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    # consumers.py

    import json
    from channels.generic.websocket import AsyncWebsocketConsumer
    from asgiref.sync import async_to_sync
    from .models import Message

    class ChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

        async def disconnect(self, close_code):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        async def receive(self, text_data):
            text_data_json = json.loads(text_data)
            message_content = text_data_json['message']

            sender = self.scope['user']
            recipient_id = int(self.room_name.split('_')[-1])
            recipient = User.objects.get(id=recipient_id)

            # Save the message to the database
            message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                content=message_content
            )

            # Send the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': {
                        'content': message.content,
                        'timestamp': str(message.timestamp),
                        'sender': message.sender.username
                    }
                }
            )

        async def chat_message(self, event):
            message = event['message']

            # Send the message to the WebSocket
            await self.send(text_data=json.dumps({
                'message': message
            }))
