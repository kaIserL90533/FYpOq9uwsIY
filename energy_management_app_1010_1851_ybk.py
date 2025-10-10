# 代码生成时间: 2025-10-10 18:51:56
import json
from django.apps import AppConfig
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path

"""
Energy Management System
"""


class EnergyManagementAppConfig(AppConfig):
    """
    Configure the Energy Management Django app.
    """
    name = 'energy_management'
    verbose_name = 'Energy Management System'

"""
Energy Management Models
"""
class EnergySource(models.Model):
    """
    Model representing an energy source.
    """
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

"""
Energy Management Views
"""
class EnergySourceListView(View):
    """
    View to handle listing energy sources.
    """
    def get(self, request):
        try:
            energy_sources = EnergySource.objects.all()
            energy_sources_list = list(energy_sources.values())
            return JsonResponse(energy_sources_list, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

"""
Energy Management URLs
"""
urlpatterns = [
    path('energy_sources/', EnergySourceListView.as_view(), name='energy-source-list'),
]
