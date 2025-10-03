# 代码生成时间: 2025-10-03 21:48:55
import json
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import path

# 模型部分
class Device(models.Model):
    """
    设备模型，用于存储与低功耗通信协议相关的设备信息。
    """
    device_id = models.CharField(max_length=255, unique=True, help_text="设备的唯一标识符")
    device_name = models.CharField(max_length=255, help_text="设备的名称")

    def __str__(self):
        return self.device_name

# 视图部分
class DeviceView(View):
    """
    处理与设备通信相关的请求。
    """
    def get(self, request):
        """
        返回设备的列表。
        """
        devices = Device.objects.all()
        data = list(devices.values('device_id', 'device_name'))
        return JsonResponse(data, safe=False)

    def post(self, request):
        """
        添加一个新的设备。
        """
        try:
            data = json.loads(request.body)
            device = Device.objects.create(**data)
            return JsonResponse({'message': 'Device created successfully', 'device_id': device.device_id}, status=201)
        except (json.JSONDecodeError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)

# URL配置
urlpatterns = [
    path('devices/', DeviceView.as_view(), name='device-list'),
]
