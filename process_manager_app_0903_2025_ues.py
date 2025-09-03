# 代码生成时间: 2025-09-03 20:25:50
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import path
from subprocess import Popen, PIPE
import json


# models.py
class Process(models.Model):
    """Model to store process information."""
    name = models.CharField(max_length=255)
    command = models.TextField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# views.py
def start_process(request, process_id):
    """Start a process with the given process_id."""
    try:
        process = Process.objects.get(id=process_id)
        if process.is_active:
            return HttpResponse("Process is already running.", status=409)
        process.is_active = True
        process.save()
        # Start the process
        process_command = process.command
        Popen(process_command, shell=True, stdout=PIPE, stderr=PIPE)
        return HttpResponse("Process started successfully.", status=200)
    except Process.DoesNotExist:
        raise Http404("Process not found.")


def stop_process(request, process_id):
    """Stop a process with the given process_id."""
    try:
        process = Process.objects.get(id=process_id)
        if not process.is_active:
            return HttpResponse("Process is not running.", status=409)
        process.is_active = False
        process.end_time = models.DateTimeField(auto_now=True)
        process.save()
        return HttpResponse("Process stopped successfully.", status=200)
    except Process.DoesNotExist:
        raise Http404("Process not found.")


def list_processes(request):
    """List all processes."""
    processes = Process.objects.all()
    process_list = [{'id': process.id, 'name': process.name} for process in processes]
    return HttpResponse(json.dumps(process_list), content_type='application/json')


# urls.py
urlpatterns = [
    path('start/<int:process_id>/', start_process, name='start_process'),
    path('stop/<int:process_id>/', stop_process, name='stop_process'),
    path('list/', list_processes, name='list_processes'),
]
