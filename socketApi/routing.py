from socketApi.consumer import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path("api/chat/<int:chat_room_id>/", ChatConsumer)
 ]