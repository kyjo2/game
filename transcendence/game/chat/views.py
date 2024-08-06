# views.py
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from .models import Message

def chat_room(request, user_id):
    # Assuming you have a way to get the logged-in user
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')
    
    context = {
        'other_user': other_user,
        'messages': messages,
    }
    return render(request, 'chat/index.html', context)

def index(request):
    return render(request, "chat/index.html")