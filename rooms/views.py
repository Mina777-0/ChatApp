from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from .models import Room, Message


def rooms(request:HttpRequest):
    rooms = Room.objects.all()

    if request.method == "POST":
        room = request.POST.get('room')

        if Room.objects.filter(name = room).exists():
            return render(request, "rooms/rooms.html", {'message': "The room already exists"})
        
        Room.objects.create(name = room)

    return render(request, "rooms/rooms.html",{'rooms':rooms})

def room(request: HttpRequest, room_name):
    room = Room.objects.get(name =  room_name)
    messages = Message.objects.filter(room= room)

    return render(request, "rooms/room.html", {'room': room, 'messages': messages})
