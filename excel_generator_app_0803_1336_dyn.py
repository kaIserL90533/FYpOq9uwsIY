# 代码生成时间: 2025-08-03 13:36:46
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.core.files.storage import default_storage
from openpyxl import Workbook
import os

"""
A Django view to generate an Excel file.
"""
class ExcelGeneratorView(View):
    """
    A view to handle Excel file generation.
    """
    def get(self, request, *args, **kwargs):
        # Create a new Excel workbook
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Generated Excel'
        worksheet.append(['Column 1', 'Column 2', 'Column 3'])  # Example header
        worksheet.append(['Row 1, Column 1', 'Row 1, Column 2', 'Row 1, Column 3'])  # Example row
        
        # Save the workbook to a file
        file_path = 'generated_excel.xlsx'
        workbook.save(file_path)
        
        # Serve the file to the user
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        with open(file_path, 'rb') as fh:
            response.write(fh.read())
        
        # Clean up the generated file
        default_storage.delete(file_path)
        
        return response

# urls.py
from django.urls import path
from .views import ExcelGeneratorView

"""
URLs for the Excel generator app.
"""
urlpatterns = [
    path('generate_excel/', ExcelGeneratorView.as_view(), name='generate_excel'),
]

# models.py
from django.db import models

"""
Django models for the Excel generator app.
"""
# If additional models are needed for data storage, they can be defined here.

# For this simple implementation, no models are required as the Excel generation
# does not involve database operations.

# However, if you need to generate Excel files based on models, you would define
# your models here and then use Django's ORM to fetch data and write it to the Excel file.

