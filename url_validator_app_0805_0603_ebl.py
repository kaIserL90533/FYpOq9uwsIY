# 代码生成时间: 2025-08-05 06:03:24
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
# 增强安全性
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import urllib.request
# TODO: 优化性能

"""
A Django app to validate the validity of URL links.
# 改进用户体验
"""
# NOTE: 重要实现细节

class Url(models.Model):
    """
# FIXME: 处理边界情况
    Model to store URL data.
    """
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class UrlValidatorView(View):
    """
    View to validate URL links.
    """
    def post(self, request, *args, **kwargs):
        """
        Validates a URL link and returns the result.
        """
        try:
            # Extract URL from the POST request
            data = request.POST.get('url')
            # Validate the URL
            URLValidator()(url=data)
            # Check if the URL is reachable
            urllib.request.urlopen(data)
            return JsonResponse({'status': 'valid', 'message': 'The URL is valid and reachable.'}, status=200)
        except ValidationError as e:
            # Handle URL validation errors
            return JsonResponse({'status': 'invalid', 'message': str(e)}, status=400)
        except Exception as e:
            # Handle other exceptions
            return JsonResponse({'status': 'invalid', 'message': 'The URL is not reachable.'}, status=400)

# URL patterns for the URL Validator app
from django.urls import path

urlpatterns = [
    path('validate/', UrlValidatorView.as_view(), name='validate_url'),
]