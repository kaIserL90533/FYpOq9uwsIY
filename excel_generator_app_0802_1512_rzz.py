# 代码生成时间: 2025-08-02 15:12:24
# excel_generator_app/__init__.py
# 这个文件通常为空，表示这是一个Django应用。

# excel_generator_app/models.py
from django.db import models

"""
Models for Excel Generator Application
"""

class DataModel(models.Model):
    """
    A simple model to store data for Excel generation.
    """
    name = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return self.name

# excel_generator_app/views.py
from django.http import HttpResponse
from django.views import View
from .models import DataModel
import xlsxwriter
import datetime

"""
Views for Excel Generator Application
"""

class ExcelExportView(View):
    """
    A class-based view to generate Excel files.
    """
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve data from the model
            data = DataModel.objects.all()

            # Create a response with an Excel file
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="exported_data_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx"'

            # Create a workbook and add a worksheet
            workbook = xlsxwriter.Workbook(response, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            # Write data to the worksheet
            worksheet.write('A1', 'Name')
            worksheet.write('B1', 'Value')
            for i, item in enumerate(data, start=2):
                worksheet.write(f'A{i}', item.name)
                worksheet.write(f'B{i}', item.value)

            # Close the workbook
            workbook.close()

            # Return the response
            return response
        except Exception as e:
            return HttpResponse(f'An error occurred: {e}', status=500)

# excel_generator_app/urls.py
from django.urls import path
from .views import ExcelExportView

"""
URLs for Excel Generator Application
"""
urlpatterns = [
    path('export/', ExcelExportView.as_view(), name='export-excel'),
]
