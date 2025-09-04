# 代码生成时间: 2025-09-04 17:39:14
import os
from django.apps import AppConfig
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json
import plotly as py
import plotly.graph_objects as go


# Model to store chart configurations
class ChartConfig(models.Model):
    title = models.CharField(max_length=200)
    x_axis_label = models.CharField(max_length=200)
    y_axis_label = models.CharField(max_length=200)
    data = models.JSONField()
    def __str__(self):
        return self.title



# View to handle chart generation
class ChartGeneratorView(View):
    """
    View to generate interactive charts.
    It receives data through POST request and returns a chart as a JSON response.
    """
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            # Validate data
            if not data.get('title') or not data.get('x_axis_label') or not data.get('y_axis_label') or not data.get('data'):
                raise ValidationError('Missing required chart configuration data')

            # Generate chart
            figure = go.Figure(data=go.Bar(x=data['data']['x'], y=data['data']['y']))
            figure.update_layout(title=data['title'], xaxis_title=data['x_axis_label'], yaxis_title=data['y_axis_label'])

            # Save chart configuration to database
            chart_config = ChartConfig(
                title=data['title'],
                x_axis_label=data['x_axis_label'],
                y_axis_label=data['y_axis_label'],
                data=data
            )
            chart_config.save()

            # Return chart as JSON
            return JsonResponse({'chart': py.offline.plot(figure, output_type='div', include_plotlyjs=True, show_link=False)})

        except (json.JSONDecodeError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)


# URL configuration for the chart generator
urlpatterns = [
    path('generate-chart/', ChartGeneratorView.as_view(), name='generate-chart'),
]


# AppConfig for the interactive_chart
class InteractiveChartConfig(AppConfig):
    name = 'interactive_chart'
    verbose_name = 'Interactive Chart Generator'