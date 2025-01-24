from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.chat_home, name='chat-home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='chat/logout.html'), name='logout'),
    path('chat/<str:username>/', views.chat_room, name='chat-room'),
]
