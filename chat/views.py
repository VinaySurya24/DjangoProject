from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import ChatMessage
from django.db.models import Q as models

# Create your views here.

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
        (models.Q(sender=request.user, receiver=other_user) |
         models.Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')
    
    return render(request, 'chat/room.html', {
        'other_user': other_user,
        'messages': messages
    })
