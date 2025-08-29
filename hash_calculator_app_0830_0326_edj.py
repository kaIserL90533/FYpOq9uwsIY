# 代码生成时间: 2025-08-30 03:26:55
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.urls import path
from hashlib import sha256
import hmac

"""
哈希值计算工具应用组件
提供对字符串进行哈希值计算的功能。
"""

class HashCalculatorView(View):
    """
    视图：计算字符串的哈希值
    """
    def get(self, request):
        """
        处理GET请求，返回表单页面
        """
        return render(request, 'hash_calculator_app/hash_form.html')
    
    def post(self, request):
        """
        处理POST请求，计算哈希值并返回结果
        """
        try:
            # 获取表单数据
            input_string = request.POST.get('input_string')
            if not input_string:
                raise ValueError("输入字符串不能为空")
            
            # 计算哈希值
            hash_value = hmac.new('secret_key'.encode(), input_string.encode(), sha256).hexdigest()
            
            # 返回JSON响应
            return JsonResponse({'status': 'success', 'hash_value': hash_value})
        except Exception as e:
            # 错误处理，返回错误信息
            return JsonResponse({'status': 'error', 'message': str(e)})

"""
URLs配置
"""
urlpatterns = [
    path('hash_calculator/', HashCalculatorView.as_view(), name='hash_calculator'),
]

# 以下是模板文件的示例内容（保存为templates/hash_calculator_app/hash_form.html）
# {% load static %}
# <!DOCTYPE html>
# <html>
# <head>
#     <title>哈希值计算工具</title>
# </head>
# <body>
#     <h1>哈希值计算工具</h1>
#     <form method="post" action="{% url 'hash_calculator' %}">
#         {% csrf_token %}
#         <input type="text" name="input_string" required>
#         <button type="submit">计算哈希值</button>
#     </form>
# </body>
# </html>