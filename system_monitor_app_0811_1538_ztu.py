# 代码生成时间: 2025-08-11 15:38:29
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.management import call_command
import psutil
import time
import threading

"""
A Django application for monitoring system performance.
This app provides views to retrieve system information such as CPU, memory, and disk usage.
"""

# Define a URL pattern for the application
urlpatterns = [
    path('cpu/', CPUView.as_view(), name='cpu_usage'),
    path('memory/', MemoryView.as_view(), name='memory_usage'),
    path('disk/', DiskView.as_view(), name='disk_usage'),
]

"""
This view returns the current CPU usage percentage.
"""
@require_http_methods(['GET'])
def cpu_usage(request):
    """
    Retrieve the current CPU usage percentage.

    Args:
        None

    Returns:
        JsonResponse: A JSON response containing the CPU usage percentage.
    """
    usage = psutil.cpu_percent(interval=1)
    return JsonResponse({'cpu_usage': usage})

"""
This view returns information about memory usage.
"""
@require_http_methods(['GET'])
def memory_usage(request):
    """
    Retrieve information about memory usage.

    Args:
        None

    Returns:
        JsonResponse: A JSON response containing memory usage information.
    """
    vms = psutil.virtual_memory()
    return JsonResponse({
        'total': vms.total / (1024 ** 3),  # GB
        'available': vms.available / (1024 ** 3),  # GB
        'used': vms.used / (1024 ** 3),  # GB
        'percentage': vms.percent,
    })

"""
This view returns information about disk usage.
"""
@require_http_methods(['GET'])
def disk_usage(request):
    """
    Retrieve information about disk usage.

    Args:
        None

    Returns:
        JsonResponse: A JSON response containing disk usage information.
    """
    disk_partitions = psutil.disk_partitions()
    disk_data = []
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_data.append({
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'total': usage.total / (1024 ** 3),  # GB
            'used': usage.used / (1024 ** 3),  # GB
            'free': usage.free / (1024 ** 3),  # GB
            'percentage': usage.percent,
        })
    return JsonResponse({'disk_usage': disk_data})
