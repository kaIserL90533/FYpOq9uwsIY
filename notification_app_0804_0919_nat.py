# 代码生成时间: 2025-08-04 09:19:38
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View


# Models
class Notification(models.Model):
    """消息通知模型"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):  # 字符串表示
        return self.title

# Views
@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class NotificationView(View):
    """消息通知视图"""
    def get(self, request):  # 获取所有通知
        notifications = Notification.objects.all()
        return JsonResponse(list(notifications.values()), safe=False)

    def post(self, request):  # 创建新的通知
        try:  # 错误处理
            title = request.POST.get('title')
            content = request.POST.get('content')
            if not title or not content:  # 数据验证
                return JsonResponse({'error': 'Missing title or content'}, status=400)

            notification = Notification(title=title, content=content)
            notification.save()
            return JsonResponse(notification.values(), status=201)
        except Exception as e:  # 通用异常处理
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, pk):  # 更新通知状态为已读
        try:  # 错误处理
            notification = Notification.objects.get(pk=pk)
            notification.read = True
            notification.save()
            return JsonResponse(notification.values())
        except ObjectDoesNotExist:  # 通知不存在
            return JsonResponse({'error': 'Notification not found'}, status=404)
        except Exception as e:  # 通用异常处理
            return JsonResponse({'error': str(e)}, status=500)

# URLs
from django.urls import path

notification_urls = [
    path('notifications/', NotificationView.as_view(), name='notifications'),
]
