# 代码生成时间: 2025-09-17 16:27:28
from django.db import models
from django.http import HttpResponse
from django.views import View
from django.urls import path
import xlsxwriter
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import datetime


# Define the models.py file with a simple model for storing data
class ExcelData(models.Model):
    """Model to store data for Excel generation"""
    data = models.TextField(help_text="Data to be stored for Excel generation")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp for when the data was created")

    def __str__(self):
        return self.data[:50]


# Define the views.py file with Excel generation logic
@method_decorator(csrf_protect, name='dispatch')
class ExcelGeneratorView(View):
    """View to handle Excel file generation"""

    def get(self, request, *args, **kwargs):
        "