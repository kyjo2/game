from django.urls import re_path

from . import gameQueueConsumers, gameConsumers

websocket_urlpatterns = [
    re_path(r'^ws/rankgames/(?P<type>[\w-]+)/$', gameQueueConsumers.RankGameRoomConsumer.as_asgi()),
    re_path(r'^ws/games/start/(?P<game_id>[a-fA-F0-9\-]{36})/(?P<type>[\w-]+)/$', gameConsumers.GameConsumer.as_asgi()),
]
# re_path(r'^game/(?P<game_id>[0-9]+)/$',