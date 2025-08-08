# 代码生成时间: 2025-08-09 01:26:16
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.conf import settings
import re
import logging

# 设置日志文件路径
LOG_FILE_PATH = getattr(settings, 'LOG_FILE_PATH', None)

# 定义日志解析异常
class LogParseError(Exception):
    pass


# 模型
class ParsedLog(models.Model):
    """存储解析后的日志条目"""
    log_entry = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.log_entry[:50]


# 视图
class LogParserView(View):
    """
    视图类，用于解析日志文件并返回结果。
    """
    def get(self, request, *args, **kwargs):
        """
        GET请求处理器，返回解析后的日志文件内容。
        """
        try:
            # 检查日志文件路径是否存在
            if not LOG_FILE_PATH:
                raise LogParseError('日志文件路径未配置。')
            
            # 读取日志文件
            with open(LOG_FILE_PATH, 'r') as file:
                log_content = file.read()
                
            # 解析日志内容（示例：按行分割）
            log_entries = log_content.split('
')
            
            # 存储解析后的日志条目到数据库
            for entry in log_entries:
                ParsedLog.objects.create(log_entry=entry)
                
            # 返回成功响应
            return JsonResponse({'message': '日志解析成功'}, status=200)
        except FileNotFoundError:
            # 文件未找到错误处理
            return JsonResponse({'error': '日志文件未找到。'}, status=404)
        except LogParseError as e:
            # 日志解析异常处理
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            # 其他异常处理
            return JsonResponse({'error': '解析日志时发生未知错误。'}, status=500)

# URL配置
urlpatterns = [
    path('parse_log/', LogParserView.as_view(), name='parse_log'),
]
