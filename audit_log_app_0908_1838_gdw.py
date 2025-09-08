# 代码生成时间: 2025-09-08 18:38:29
# audit_log_app\application.py
from django.apps import AppConfig

class AuditLogAppConfig(AppConfig):
    name = 'audit_log_app'
    verbose_name = 'Security Audit Log Application'

# audit_log_app\models.py
from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    """
    A model to store security audit logs.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AuditLog for {self.user.username} at {self.timestamp}"

# audit_log_app\views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import AuditLog
from django.contrib.auth.decorators import login_required

@require_http_methods(['POST'])
@login_required
def log_audit(request):
    """
    Create a new audit log entry.
    """
    try:
        action = request.POST.get('action')
        description = request.POST.get('description')

        if not action or not description:
            raise ValueError('Action and description are required.')

        AuditLog.objects.create(
            user=request.user,
            action=action,
            description=description
        )
        return JsonResponse({'message': 'Audit log created successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# audit_log_app\urls.py
from django.urls import path
from .views import log_audit

urlpatterns = [
    path('log/', log_audit, name='log_audit'),
]
