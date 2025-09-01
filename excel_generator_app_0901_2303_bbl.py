# 代码生成时间: 2025-09-01 23:03:28
import os
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .models import DataModel
from .forms import DataForm
from openpyxl import Workbook

# Model
class DataModel(models.Model):
    """Model to store data for the Excel generator."""
    data = models.CharField(max_length=255)

    def __str__(self):
        return self.data

# Form
class DataForm(forms.ModelForm):
    """Form for inputting data to generate Excel file."""
    class Meta:
        model = DataModel
        fields = ('data',)

# View
class ExcelGeneratorView(View):
    """View to generate Excel file based on form input."""
    template_name = 'excel_generator.html'
    form_class = DataForm

    def get(self, request, *args, **kwargs):
        """Handle GET request to show the form."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST request to process form data and generate Excel file."""
        form = self.form_class(request.POST)
        if form.is_valid():
            wb = Workbook()
            ws = wb.active
            ws.title = 'Data'
            ws.append(['Data'])
            # Assuming one data entry for simplicity
            ws.append([form.cleaned_data['data']])
            filename = 'data.xlsx'
            wb.save(os.path.join(settings.MEDIA_ROOT, filename))
            return HttpResponse('Excel file generated successfully.', status=200)
        else:
            return render(request, self.template_name, {'form': form})

# URL configuration
from django.urls import path

urlpatterns = [
    path('generate/', ExcelGeneratorView.as_view(), name='excel_generator'),
]

# Templates
# excel_generator.html
# {% extends "base.html" %}
# {% block content %}
#     <h2>Excel Generator</h2>
#     <form method="post" enctype="multipart/form-data">
#         {% csrf_token %}
#         {{ form.as_p }}
#         <button type="submit">Generate Excel</button>
#     </form>
# {% endblock %}