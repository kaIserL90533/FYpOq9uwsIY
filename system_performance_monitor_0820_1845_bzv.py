# 代码生成时间: 2025-08-20 18:45:53
import psutil
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path

"""
系统性能监控工具 Django 应用组件
"""

# Models
# 优化算法效率
class SystemPerformance(models.Model):
    """
    系统性能数据模型，存储 CPU，内存，磁盘等数据
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    network_sent = models.BigIntegerField()
    network_received = models.BigIntegerField()

    def __str__(self):
        return f"SystemPerformance at {self.timestamp}"


# Views
class SystemPerformanceView(View):
    """
    系统性能监控视图
    """
    def get(self, request, *args, **kwargs):
        try:
            # 获取系统性能数据
            cpu = psutil.cpu_percent(interval=1)
# 改进用户体验
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
# 增强安全性
            network_io = psutil.net_io_counters()
# 改进用户体验
            response_data = {
                'cpu_usage': cpu,
                'memory_usage': memory,
                'disk_usage': disk,
                'network_sent': network_io.bytes_sent,
                'network_received': network_io.bytes_recv,
            }
            return JsonResponse(response_data)
        except Exception as e:
            # 错误处理
# TODO: 优化性能
            return JsonResponse({'error': str(e)}, status=500)


# URLs
urlpatterns = [
    path('system-performance/', SystemPerformanceView.as_view(), name='system_performance'),
]
# 扩展功能模块
