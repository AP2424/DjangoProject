from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from directchat.models import ChatRoom, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        self.room = ChatRoom.objects.get(name=self.room_name)
        if (self.user not in self.room.users.all()):
            self.close()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        if type == 'create':
            message = text_data_json['message']
            author = text_data_json['author']
            editedMessageID = text_data_json['editedMessageID']
            if int(editedMessageID) == 0:
                mess_obj = Message(room=self.room, text=message, author=User.objects.get(username=author))
                mess_obj.save()
            else:
                mess_obj = Message.objects.get(id=editedMessageID)
                mess_obj.text = message
                mess_obj.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'author': author,
                    'messageID': mess_obj.id,
                    'editedMessageID': editedMessageID
                }
            )



    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def chat_message(self, event):
        message = event['message']
        author = event['author']
        messageID = event['messageID']
        editedMessageID = event['editedMessageID']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'author': author,
            'messageID': messageID,
            'editedMessageID': editedMessageID
        }))


