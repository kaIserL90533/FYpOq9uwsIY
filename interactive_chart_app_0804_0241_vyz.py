# 代码生成时间: 2025-08-04 02:41:11
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db import models
from django.urls import path
from django.core.exceptions import ValidationError
import json

# Models
class Chart(models.Model):
    """Model to store chart configurations."""
    chart_name = models.CharField(max_length=255)
    data = models.TextField()  # JSON string representing the chart data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chart_name

# Views
class ChartView(View):
    """View to handle chart generation and interaction."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests to display the chart form."""
        return render(request, 'chart_form.html')

    def post(self, request, *args, **kwargs):
        """Handle POST requests to generate the chart."""
        try:
            chart_name = request.POST.get('chart_name')
            chart_data = json.loads(request.POST.get('chart_data'))
            
            # Save chart configuration to the database
            chart = Chart(chart_name=chart_name, data=json.dumps(chart_data))
            chart.full_clean()  # Check for any validation errors
            chart.save()
            
            # Return chart data as JSON
            return JsonResponse({'message': 'Chart created successfully.', 'chart_id': chart.id})
        except (json.JSONDecodeError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)

# URL Patterns
urlpatterns = [
    path('chart/', ChartView.as_view(), name='chart_view'),
]

# Template example for chart_form.html
# {% extends "base.html" %}
# {% block content %}
# <form method="post" action="{% url 'chart_view' %}">
#     <label for="chart_name">Chart Name:</label>
#     <input type="text" id="chart_name" name="chart_name" required>
#     <label for="chart_data">Chart Data (JSON):</label>
#     <textarea id="chart_data" name="chart_data" required></textarea>
#     <button type="submit">Generate Chart</button>
# </form>
# {% endblock %}