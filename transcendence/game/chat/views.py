# views.py
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message

def chat_room(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    # 메시지들을 문자열로 변환, 필드 이름 'content'로 수정
    messages_text = "\n".join([f"{msg.sender.username}: {msg.content}" for msg in messages])

    context = {
        'other_user': other_user,
        'messages_text': messages_text,  # 변환된 메시지 문자열
    }
    return render(request, 'chat/room.html', context)


def index(request):
    return render(request, "chat/index.html")

@login_required
def user_list_view(request):
    current_user = request.user  # 현재 로그인된 사용자
    users = User.objects.exclude(id=current_user.id)
    return render(request, 'chat/user_list.html', {'users': users})