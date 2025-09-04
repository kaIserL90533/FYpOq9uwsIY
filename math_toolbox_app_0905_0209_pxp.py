# 代码生成时间: 2025-09-05 02:09:36
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
"""
数学计算工具集应用
支持基本数学计算功能
"""

# models.py
class CalculationModel(models.Model):
    expression = models.CharField(max_length=255)
    """保存数学表达式"""
    result = models.FloatField()
    """保存计算结果"""

    def __str__(self):
        return f"{self.expression} = {self.result}"

# views.py
class MathToolView(View):
    """数学计算工具视图"""
    def post(self, request, *args, **kwargs):
        """处理POST请求，执行数学计算并返回结果"""
        expression = request.POST.get('expression')
        if not expression:
            return JsonResponse({'error': 'Missing expression'}, status=400)

        try:
            result = eval(expression)
        except (SyntaxError, NameError, ZeroDivisionError) as e:
            return JsonResponse({'error': str(e)}, status=400)

        calculation = CalculationModel()
        calculation.expression = expression
        calculation.result = result
        calculation.save()

        return JsonResponse({'expression': expression, 'result': result})

# urls.py
math_toolbox_patterns = [
    path('calculate/', csrf_exempt(MathToolView.as_view()), name='calculate'),
]

# 使用时请确保将此urls.py文件包含到项目的urls.py中。