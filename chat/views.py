from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import ChatMessage
from django.db.models import Q
from django.http import JsonResponse
import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def chat_home(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat/home.html', {'users': users})

@login_required
def chat_room(request, username):
    other_user = User.objects.get(username=username)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user, receiver=other_user) |
         Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')
    
    users = User.objects.exclude(username=request.user.username)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message
            )
            return redirect('chat-room', username=username)
    
    return render(request, 'chat/room.html', {
        'other_user': other_user,
        'messages': messages,
        'users': users
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        receiver = User.objects.get(username=data['receiver'])
        message = data['message']
        
        chat_message = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message
        )
        
        return JsonResponse({
            'status': 'success',
            'message': message,
            'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_messages(request, username):
    other_user = User.objects.get(username=username)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user, receiver=other_user) |
         Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')
    
    message_list = [{
        'sender': msg.sender.username,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages]
    
    return JsonResponse({'messages': message_list})
