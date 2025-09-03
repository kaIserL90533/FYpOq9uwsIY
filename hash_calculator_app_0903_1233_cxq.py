# 代码生成时间: 2025-09-03 12:33:25
from django.conf.urls import url
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5, sha1, sha256, sha512
import json

# Models
class HashCalculator(models.Model):
    """
    A model that represents a hash calculation request.
    Attributes:
    - input_string (str): The string to be hashed.
    - algorithm (str): The hashing algorithm to use (md5, sha1, sha256, sha512).
    - result (str): The resulting hash.
    """
    input_string = models.CharField(max_length=1024)
    algorithm = models.CharField(max_length=10)
    result = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        # Calculate the hash when the model instance is saved.
        self.result = self.calculate_hash(self.input_string, self.algorithm)
        super(HashCalculator, self).save(*args, **kwargs)
    @staticmethod
    def calculate_hash(input_string, algorithm):
        """
        Calculates the hash of the input string using the specified algorithm.
        Args:
        - input_string (str): The string to be hashed.
        - algorithm (str): The hashing algorithm to use.
        Returns:
        - str: The resulting hash.
        Raises:
        - ValueError: If the algorithm is not supported.
        """
        if algorithm == 'md5':
            return md5(input_string.encode()).hexdigest()
        elif algorithm == 'sha1':
            return sha1(input_string.encode()).hexdigest()
        elif algorithm == 'sha256':
            return sha256(input_string.encode()).hexdigest()
        elif algorithm == 'sha512':
            return sha512(input_string.encode()).hexdigest()
        else:
            raise ValueError('Unsupported algorithm')

# Views
@method_decorator(csrf_exempt, name='dispatch')
class HashCalculatorView(View):
    """
    A view that receives a POST request with an input string and a hashing algorithm,
    and returns the resulting hash.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            input_string = data.get('input_string')
            algorithm = data.get('algorithm')
            if not input_string or not algorithm:
                raise ValidationError('Input string and algorithm are required')

            hash_result = HashCalculator.calculate_hash(input_string, algorithm)
            return JsonResponse({'hash': hash_result})
        except (ValueError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

# URLs
urlpatterns = [
    url(r'^hash/$', HashCalculatorView.as_view(), name='hash_calculator'),
]
