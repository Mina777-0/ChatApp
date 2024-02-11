import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Room, Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    #join the room
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

    #leave the room
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )


    
    #receive message from the websocket
    #json.loads converts the json string from stringfy(js object html-file) and store it in the text_data, 
    #then we store that in data as a dictionary. so message takes the value of the key (message) whcih is message 
    #and store it in message. the same for username
    
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        self.save_message(username, room, message)

        print("message", message)
        print('user', username)

        #send the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

    #receive the message from the group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

    #send the message to the websocket by dumping it
        self.send(json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username,
            'room': room,
        }))

    def save_message(self, username, room, message):
        user = User.objects.get(username= username)
        room = Room.objects.get(name = room)
        message = Message.objects.create(user = user, room= room, content = message)



#It is important to note that separate instances of ChatConsumer run the methods receive and chat_message, 
#hence the self.user in those methods are different. While the receive method is executed in the sender's channel, 
#the chat_message method is executed in the channels of the receivers which will also include the sender in this case, 
#since he is in the same group as the receivers. 