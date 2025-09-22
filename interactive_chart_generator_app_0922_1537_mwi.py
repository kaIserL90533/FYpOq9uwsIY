# 代码生成时间: 2025-09-22 15:37:38
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.urls import path
from asgiref.sync import sync_to_async
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import ChartData
from .forms import ChartForm
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Define the ChartView class for generating interactive charts
class ChartView(View):
    """A view to handle chart data generation and rendering."""

    def get(self, request, *args, **kwargs):
        """Handle GET request to display the chart form."""
        form = ChartForm()
        return render(request, 'chart_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST request to generate the chart based on user input."""
        form = ChartForm(request.POST)
        if form.is_valid():
            chart_type = form.cleaned_data.get('chart_type')
            data = fetch_chart_data(chart_type)
            if data:
                return self.render_chart(chart_type, data)
            else:
                return JsonResponse({'error': 'No data available for the selected chart type.'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid form data.'}, status=400)

    def render_chart(self, chart_type, data):
        """Render the chart based on the type and data."""
        try:
            fig, ax = plt.subplots()
            if chart_type == 'line':
                ax.plot(data['x'], data['y'])
            elif chart_type == 'bar':
                ax.bar(data['x'], data['y'])
            # ... add more chart types as needed
            else:
                return JsonResponse({'error': 'Unsupported chart type.'}, status=400)

            canvas = FigureCanvasAgg(fig)
            canvas.draw()
            buf = io.BytesIO()
            canvas.print_png(buf)
            buf.seek(0)
            return HttpResponse(buf, content_type='image/png')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Define the function to fetch chart data from the database
@sync_to_async
def fetch_chart_data(chart_type):
    """Fetch data for the chart from the database based on the chart type."""
    try:
        return ChartData.objects.get(chart_type=chart_type).data
    except ObjectDoesNotExist:
        return None

# Define the chart data model
class ChartData(models.Model):
    """Model to store chart data."""
    chart_type = models.CharField(max_length=100)
    data = models.JSONField()

    def __str__(self):
        return f'{self.chart_type} Chart Data'

# Define the chart form
class ChartForm(forms.ModelForm):
    """Form to input chart details."""
    chart_type = forms.ChoiceField(choices=[('line', 'Line'), ('bar', 'Bar')])

    class Meta:
        fields = ['chart_type']

# Define the URL patterns
urlpatterns = [
    path('chart/', ChartView.as_view(), name='chart'),
]