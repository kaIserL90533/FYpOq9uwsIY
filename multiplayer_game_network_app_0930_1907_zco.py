# 代码生成时间: 2025-09-30 19:07:50
# multiplayer_game_network_app/models.py
"""Models for the multiplayer game network application."""
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    """Model representing a game."""
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_games')
    players = models.ManyToManyField(User, related_name='games', blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    """Model representing a message in the game."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}..."

# multiplayer_game_network_app/views.py
"""Views for the multiplayer game network application."""
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from .models import Game, Message
from django.contrib.auth.decorators import login_required

@require_http_methods(['GET', 'POST'])
@login_required
def game_list(request):
    """View to list games and create a new game."""
    if request.method == 'POST':
        # Create a new game
        game = Game.objects.create(name=request.POST.get('name'), created_by=request.user)
        return JsonResponse({'id': game.id, 'name': game.name})
    # List existing games
    games = Game.objects.filter(created_by=request.user)
    return render(request, 'game_list.html', {'games': games})

@require_http_methods(['GET', 'POST'])
@login_required
def game_message(request, game_id):
    """View to send and retrieve messages in a game."""
    if request.method == 'POST':
        # Send a message
        message = Message.objects.create(game_id=game_id, sender=request.user, content=request.POST.get('content'))
        return JsonResponse({'id': message.id, 'content': message.content})
    # Retrieve messages for a game
    messages = Message.objects.filter(game_id=game_id).order_by('-timestamp')
    return render(request, 'game_messages.html', {'messages': messages})

# multiplayer_game_network_app/urls.py
"""URLs for the multiplayer game network application."""
from django.urls import path
from .views import game_list, game_message

app_name = 'game_network'
urlpatterns = [
    path('games/', game_list, name='game_list'),
    path('game/<int:game_id>/messages/', game_message, name='game_message'),
]

# multiplayer_game_network_app/tests.py
"""Tests for the multiplayer game network application."""
from django.test import TestCase
from .models import Game, Message
from django.contrib.auth.models import User

class GameNetworkTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.game = Game.objects.create(name='Test Game', created_by=self.user)
    
    def test_game_creation(self):
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(self.game.name, 'Test Game')
    
    def test_message_creation(self):
        message = Message.objects.create(game=self.game, sender=self.user, content='Hello World')
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.content, 'Hello World')
