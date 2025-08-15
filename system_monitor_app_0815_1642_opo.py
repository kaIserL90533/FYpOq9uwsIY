# 代码生成时间: 2025-08-15 16:42:07
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
import psutil
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)


# Models
class SystemInfo(models.Model):
    """Model to store system performance data."""
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SystemInfo(cpu={self.cpu_usage}, memory={self.memory_usage}, disk={self.disk_usage}, timestamp={self.timestamp})"


# Views
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class SystemMonitorView(View):
    """View to monitor system performance."""

    @method_decorator(csrf_exempt, name='dispatch')
    def get(self, request, *args, **kwargs):
        """Handle GET request to get system performance data."""
        try:
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent

            system_info = SystemInfo(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage
            )
            system_info.save()

            data = {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage
            }
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"Error monitoring system performance: {e}")
            return JsonResponse({'error': str(e)}, status=500)

# URLs
from django.urls import path

urlpatterns = [
    path('monitor/', SystemMonitorView.as_view(), name='system_monitor'),
]
