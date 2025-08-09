# 代码生成时间: 2025-08-10 06:24:04
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
import psutil
import os


# 模型类
class SystemInfo(models.Model):
    """存储系统信息模型"""
    timestamp = models.DateTimeField(auto_now_add=True)
    total_memory = models.BigIntegerField()
    used_memory = models.BigIntegerField()
    free_memory = models.BigIntegerField()
    memory_usage_percent = models.FloatField()

    def __str__(self):
        return f"SystemInfo at {self.timestamp}"


# 视图类
class MemoryUsageView(View):
    """内存使用情况分析视图"""
    def get(self, request, *args, **kwargs):
        """处理GET请求，返回内存使用情况分析"""
        try:
            # 获取系统内存信息
            memory = psutil.virtual_memory()
            total_memory = memory.total
            used_memory = memory.used
            free_memory = memory.free
            memory_usage_percent = memory.percent

            # 存储系统信息
            system_info = SystemInfo.objects.create(
                total_memory=total_memory,
                used_memory=used_memory,
                free_memory=free_memory,
                memory_usage_percent=memory_usage_percent,
            )

            # 构建返回数据
            response_data = {
                "timestamp": system_info.timestamp.isoformat(),
                "total_memory": system_info.total_memory,
                "used_memory": system_info.used_memory,
                "free_memory": system_info.free_memory,
                "memory_usage_percent": system_info.memory_usage_percent,
            }

            return JsonResponse(response_data)
        except Exception as e:
            # 错误处理
            return JsonResponse({"error": str(e)}, status=500)


# URL配置
urlpatterns = [
    path('memory_usage/', MemoryUsageView.as_view(), name='memory_usage'),
]
