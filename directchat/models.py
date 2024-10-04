from django.db import models
from users.models import User
from fantasy.models import Team


"""class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name"""

class Room(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, blank=True)


class ChatRoom(Room):
    pass

    def __str__(self):
        return self.name



class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



    def __str__(self):
        return f'{self.text} ({self.timestamp})'
