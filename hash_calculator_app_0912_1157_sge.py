# 代码生成时间: 2025-09-12 11:57:54
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
import hashlib
import hmac

# Models
class HashValue(models.Model):
    """
    Simple model to store hash values.
    """
    original_value = models.CharField(max_length=255)
    hash_value = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate and store the hash value.
        """
        if self.original_value:
            self.hash_value = self.calculate_hash(self.original_value)
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_hash(value):
        """
        Calculate a hash value using SHA-256.
        """
        return hashlib.sha256(value.encode()).hexdigest()

# Views
@method_decorator(require_http_methods(['POST']), name='dispatch')
def hash_calculator(request):
    """
    A view that calculates and returns the hash value of the input.
    """
    try:
        data = request.POST.get('data')
        if not data:
            raise ValidationError('No data provided for hashing.')
        hash_value = HashValue.calculate_hash(data)
        return JsonResponse({'original_data': data, 'hash_value': hash_value})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

# URLs
from django.urls import path

urlpatterns = [
    path('hash/', hash_calculator, name='hash_calculator'),
]
