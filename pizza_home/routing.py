from django.urls import path,re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chatroom/chat/', consumers.ChatConsumer.as_asgi()),
    path(r'ws/pizza/<order_id>', consumers.OrderProgress.as_asgi()),  
]