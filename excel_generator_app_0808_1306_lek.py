# 代码生成时间: 2025-08-08 13:06:14
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from openpyxl import Workbook
import os

# models.py
"""
Define the Data Model for Excel Generator
"""
from django.db import models

class ExcelData(models.Model):
    # This model can be extended with fields that represent data to be included in the Excel file
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title

# views.py
"""
Views for the Excel Generator Application
"""
from django.core.files import File
from openpyxl import Workbook
from .models import ExcelData
from django.http import HttpResponse

class ExcelGeneratorView(View):
    """
    View to generate and download an Excel file containing data from the ExcelData model.
    """
    def get(self, request, *args, **kwargs):
        try:
            # Create a new Excel workbook
            wb = Workbook()
            # Add a worksheet
            ws = wb.active
            # Set the title of the worksheet
            ws.title = 'Data'
            
            # Retrieve data from the model
            data = ExcelData.objects.all()
            for i, obj in enumerate(data, start=1):
                # Write data to the worksheet
                ws.append([obj.title, obj.description])
            
            # Create a file-like object to save the Excel file
            excel_file = ContentFile()
            wb.save(excel_file)
            excel_file.seek(0)
            
            # Send the Excel file as a response
            response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            return response
        except Exception as e:
            # Handle any error that occurs and return an error message
            return HttpResponse(f'An error occurred: {e}', status=500)

# urls.py
"""
URL patterns for the Excel Generator Application
"""
from django.urls import path
from .views import ExcelGeneratorView

urlpatterns = [
    path('generate_excel/', ExcelGeneratorView.as_view(), name='generate_excel'),
]
