# 代码生成时间: 2025-10-11 01:37:25
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
from django.core.exceptions import ObjectDoesNotExist


# Models
class Character(models.Model):
    """Model representing a character in the animation system."""
    name = models.CharField(max_length=100, help_text="Character's name")
    description = models.TextField(help_text="Character's description")

    def __str__(self):
        return self.name


class Animation(models.Model):
    """Model representing an animation for a character."""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='animations', help_text="The character this animation belongs to")
    name = models.CharField(max_length=100, help_text="Animation's name")
    description = models.TextField(help_text="Animation's description")
    sequence = models.JSONField(help_text="Animation sequence in JSON format")

    def __str__(self):
        return f"{self.name} for {self.character.name}"


# Views
class CharacterListView(View):
    """View for listing all characters."""
    def get(self, request, *args, **kwargs):
        characters = Character.objects.all()
        return render(request, 'character_list.html', {'characters': characters})


class CharacterDetailView(View):
    """View for displaying a single character's details."""
    def get(self, request, character_id, *args, **kwargs):
        try:
            character = Character.objects.get(pk=character_id)
            animations = character.animations.all()
            return render(request, 'character_detail.html', {'character': character, 'animations': animations})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Character not found'}, status=404)


# URLs
urlpatterns = [
    path('characters/', CharacterListView.as_view(), name='character_list'),
    path('characters/<int:character_id>/', CharacterDetailView.as_view(), name='character_detail'),
]

