# 代码生成时间: 2025-08-10 01:31:32
from django.conf.urls import url
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json

# Models
# 这里不需要数据库模型，因为我们只是计算哈希值，不存储数据

# Views
class HashCalculatorView(View):
    """
    A Django view for calculating hash values of given data.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super(HashCalculatorView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to calculate hash values.
        """
        try:
            data = json.loads(request.body)
            if not isinstance(data, dict) or 'text' not in data:
                raise ValidationError('Invalid input data. Please provide a JSON object with a 