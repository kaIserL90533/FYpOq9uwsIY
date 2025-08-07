# 代码生成时间: 2025-08-07 21:26:09
from django.http import JsonResponse
from django.views import View
from django.urls import path
import hashlib
import json

# models.py
# 这里可以定义与哈希值计算相关的模型，本例中不需要


# views.py
class HashCalculatorView(View):
    """
    视图类用于计算哈希值。
    
    这个视图接受GET请求，其中包含需要计算哈希的数据。
    它返回JSON响应，其中包含原始数据及其哈希值。
    """
    def get(self, request, *args, **kwargs):
        # 获取查询参数
        data = request.GET.get('data')
        if not data:
            return JsonResponse({'error': 'No data provided.'}, status=400)
        
        # 计算哈希值
        hash_value = hashlib.sha256(data.encode()).hexdigest()
        
        # 返回JSON响应
        return JsonResponse({'original_data': data, 'hash_value': hash_value})


# urls.py
urlpatterns = [
    path('hash_calculator/', HashCalculatorView.as_view(), name='hash_calculator'),
]
