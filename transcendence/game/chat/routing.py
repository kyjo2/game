# routing.py
from django.urls import re_path
from . import chatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>\w+)/$', chatConsumer.ChatConsumer.as_asgi()),
]
