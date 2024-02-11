from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Room(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    content = models.TextField()
    stamptime = models.DateTimeField(default= now)

    def __str__(self):
        return f"{self.room}({self.user}): {self.stamptime}"