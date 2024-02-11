from django.urls import path
from . import views

urlpatterns = [
    path('rooms', views.rooms, name="rooms"),
    path('room/<str:room_name>', views.room, name="room"),
]