# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.user_list_view, name='user_list'),
    path("room/<int:user_id>/", views.chat_room, name='room'),
]