# 代码生成时间: 2025-09-02 04:42:58
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
import re
from datetime import datetime

# 日志文件解析工具应用组件配置
class LogParserAppConfig:
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'log_parser_app'

    def ready(self):
        try:
            # 检查配置
            self.check_settings()
        except ImproperlyConfigured as e:
            # 记录错误日志
            print(f"Error: {e}")
            # 抛出异常
            raise

    def check_settings(self):
        # 验证日志文件路径配置
        required_settings = ['LOG_FILE_PATH']
        for setting in required_settings:
            if not hasattr(settings, setting):
                raise ImproperlyConfigured(f"{setting} is not defined in settings")
            if not os.path.exists(getattr(settings, setting)):
                raise ImproperlyConfigured(f"{setting} does not exist or is not accessible")

# 模型
class LogEntry(models.Model):
    timestamp = models.DateTimeField(verbose_name='Timestamp')
    log_level = models.CharField(max_length=10, verbose_name='Log Level')
    message = models.TextField(verbose_name='Message')

    class Meta:
        db_table = 'log_entries'
        verbose_name = 'Log Entry'
        verbose_name_plural = 'Log Entries'

    def __str__(self):
        return f"Log Entry ({self.timestamp}): {self.message}"

# 视图
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def parse_log_file(request):
    try:
        with open(settings.LOG_FILE_PATH, 'r') as file:
            log_entries = []
            for line in file:
                # 假设日志文件格式为：[timestamp] [log_level] message
                match = re.match(r'\[(?P<timestamp>\d+)\] \[(?P<log_level>\w+)\] (?P<message>.*)', line)
                if match:
                    log_entries.append({
                        'timestamp': datetime.fromtimestamp(int(match.group('timestamp'))),
                        'log_level': match.group('log_level'),
                        'message': match.group('message')
                    })
            return JsonResponse({'log_entries': log_entries}, safe=False)
    except FileNotFoundError:
        return HttpResponse("Log file not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error parsing log file: {str(e)}", status=500)

# URL配置
from django.urls import path

urlpatterns = [
    path('parse/', parse_log_file, name='parse_log_file')
]