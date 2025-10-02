# 代码生成时间: 2025-10-03 03:34:30
# dictionary_manager_app/__init__.py
# This file makes the directory a package.

# dictionary_manager_app/apps.py
"""
App configuration for the dictionary manager.
"""
from django.apps import AppConfig

class DictionaryManagerConfig(AppConfig):
    name = 'dictionary_manager_app'
    verbose_name = 'Dictionary Manager'

# dictionary_manager_app/models.py
"""
Models for the dictionary manager.
"""
from django.db import models

class Dictionary(models.Model):
    """
    A model for a data dictionary.
    """
    name = models.CharField(max_length=255, help_text="The name of the dictionary.")
    description = models.TextField(blank=True, help_text="A brief description of the dictionary.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The timestamp when the dictionary was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The timestamp when the dictionary was last updated.")

    def __str__(self):
        return self.name

class Entry(models.Model):
    """
    A model for an entry within a dictionary.
    """
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name='entries')
    key = models.CharField(max_length=255, unique=True, help_text="The key for the entry.")
    value = models.CharField(max_length=255, help_text="The value associated with the key.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The timestamp when the entry was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The timestamp when the entry was last updated.")

    def __str__(self):
        return f"{self.dictionary.name}: {self.key}"

# dictionary_manager_app/views.py
"""
Views for the dictionary manager.
"""
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Dictionary, Entry

class DictionaryListView(View):
    """
    A view to list all dictionaries.
    """
    def get(self, request):
        dictionaries = Dictionary.objects.all()
        return JsonResponse(list(dictionaries.values()), safe=False)

class DictionaryDetailView(View):
    """
    A view to retrieve a specific dictionary by id.
    """
    def get(self, request, dictionary_id):
        dictionary = get_object_or_404(Dictionary, pk=dictionary_id)
        return JsonResponse(dictionary.to_dict(), safe=False)

class EntryListView(View):
    """
    A view to list all entries for a given dictionary.
    """
    def get(self, request, dictionary_id):
        dictionary = get_object_or_404(Dictionary, pk=dictionary_id)
        entries = dictionary.entries.all()
        return JsonResponse(list(entries.values()), safe=False)

class EntryDetailView(View):
    """
    A view to retrieve a specific entry by key in a dictionary.
    """
    def get(self, request, dictionary_id, key):
        dictionary = get_object_or_404(Dictionary, pk=dictionary_id)
        entry = get_object_or_404(Entry, dictionary=dictionary, key=key)
        return JsonResponse(entry.to_dict(), safe=False)

# dictionary_manager_app/urls.py
"""
URLs for the dictionary manager.
"""
from django.urls import path
from .views import DictionaryListView, DictionaryDetailView, EntryListView, EntryDetailView

urlpatterns = [
    path('dictionaries/', DictionaryListView.as_view(), name='dictionary-list'),
    path('dictionaries/<int:dictionary_id>/', DictionaryDetailView.as_view(), name='dictionary-detail'),
    path('dictionaries/<int:dictionary_id/entries/', EntryListView.as_view(), name='entry-list'),
    path('dictionaries/<int:dictionary_id/entries/<str:key>/', EntryDetailView.as_view(), name='entry-detail'),
]

# dictionary_manager_app/admin.py
"""
Admin configuration for the dictionary manager.
"""
from django.contrib import admin
from .models import Dictionary, Entry

@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('dictionary', 'key', 'value', 'created_at', 'updated_at')