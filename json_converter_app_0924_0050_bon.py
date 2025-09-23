# 代码生成时间: 2025-09-24 00:50:36
from django.db import models
from django.http import JsonResponse
from django.views.generic import View
from django.urls import path
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Models
class JSONConversion(models.Model):
    """
    Model to store JSON conversion logs.
    """
    input_json = models.TextField(help_text="Input JSON data to be converted.")
    converted_json = models.TextField(help_text="Converted JSON data.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"JSON Conversion {self.id}"

# Views
@method_decorator(csrf_exempt, name='dispatch')
class JSONConverterView(View):
    """
    A view to handle JSON conversion requests.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to convert JSON data.
        """
        try:
            input_data = json.loads(request.body)
            output_data = json.dumps(input_data, ensure_ascii=False)
            JSONConversion.objects.create(input_json=json.dumps(input_data), converted_json=output_data)
            return JsonResponse({'message': 'Conversion successful', 'converted_json': output_data})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON input'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred during conversion'}, status=500)

# URLs
urlpatterns = [
    path('convert/', JSONConverterView.as_view(), name='json_converter'),
]
