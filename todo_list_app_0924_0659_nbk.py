# 代码生成时间: 2025-09-24 06:59:06
from django.db import models
from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


# 数据模型设计
class Task(models.Model):
    """A task to be completed."""
    title = models.CharField(max_length=255, help_text="Enter a title for the task.")
    description = models.TextField(blank=True, help_text="Enter a description for the task.")
    completed = models.BooleanField(default=False, help_text="Mark the task as completed.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the task was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time the task was last updated.")

    def __str__(self):
        """Return a string representation of the task."""
        return self.title


# 视图
class TaskListView(View):
    """View to list all tasks."""
    def get(self, request, *args, **kwargs):
        "