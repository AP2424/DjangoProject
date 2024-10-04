from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import FanClub
from directchat.models import Message
from fantasy.models import Team
from django.contrib.auth.models import User


class FanclubConsumer(WebsocketConsumer):
    def connect(self):
        self.fanclub_name = self.scope['url_route']['kwargs']['fanclub_name']
        self.fanclub_group_name = f'chat_{self.fanclub_name}'
        self.user = self.scope['user']
        self.fanclub = FanClub.objects.get(team=Team.objects.get(name=self.fanclub_name))
        if (self.user not in self.fanclub.users.all()):
            self.close()

        async_to_sync(self.channel_layer.group_add)(
            self.fanclub_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = text_data_json['author']
        editedMessageID = text_data_json['editedMessageID']
        async_to_sync(self.channel_layer.group_send)(
            self.fanclub_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': author,
                'editedMessageID': editedMessageID
            }
        )
        if int(editedMessageID) == 0:
            mess_obj = Message(room=self.fanclub, text=message, author=User.objects.get(username=author))
            mess_obj.save()
        else:
            mess_obj = Message.objects.get(id=editedMessageID)
            mess_obj.text = message
            mess_obj.save()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.fanclub_group_name,
            self.channel_name
        )

    def chat_message(self, event):
        message = event['message']
        author = event['author']
        editedMessageID = event['editedMessageID']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'author': author,
            'editedMessageID': editedMessageID
        }))


