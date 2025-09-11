# 代码生成时间: 2025-09-11 11:10:17
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet
import json

"""
API响应格式化工具，用于返回统一的API响应格式。
"""

class ApiResponseFormatterMixin:
    """
    Mixin类，提供统一的API响应格式化方法。
    """
    def success_response(self, data, message="Success"):
        """
        返回成功的响应。
        
        参数:
        data -- 要返回的数据
        message -- 提示信息
        """
        return JsonResponse({
            "status": "success",
            "message": message,
            "data": data
        })

    def error_response(self, message="Error", error_code=400):
        """
        返回错误的响应。
        
        参数:
        message -- 错误信息
        error_code -- 错误码，默认为400
        """
        return JsonResponse({
            "status": "error",
            "message": message,
            "error_code": error_code
        }, status=error_code)

    def format_data(self, queryset: QuerySet):
        "