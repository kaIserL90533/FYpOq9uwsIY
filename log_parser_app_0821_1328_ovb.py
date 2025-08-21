# 代码生成时间: 2025-08-21 13:28:45
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import logging
import re
import json
from typing import Dict, Any

# Django model for storing log data
class LogEntry(models.Model):
    """
    Model to store log entries.
    Each log entry contains timestamp, log level, and message.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    log_level = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return f"LogEntry: {self.timestamp}, {self.log_level}, {self.message}..."

# Django view for parsing logs and returning parsed data
class LogParserView(View):
    """
    A Django view that parses log files and returns the parsed data.
    It expects a JSON payload with the log content to parse.
    """
    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handles POST requests to parse log data.
        Expects a JSON payload with the log content.
        Returns JSON with parsed log data.
        """
        try:
            data = json.loads(request.body)
            log_content = data.get('log_content', '')
            parsed_logs = self.parse_logs(log_content)
            return JsonResponse({'parsed_logs': parsed_logs}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            logging.error(f"Error parsing log: {str(e)}")
            return JsonResponse({'error': 'Failed to parse log'}, status=500)

    def parse_logs(self, log_content: str) -> Dict[str, Any]:
        """
        Parses log content into a list of log entries.
        Each log entry is a dictionary containing the timestamp, log level, and message.
        """
        pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(\w+)\] (.*)'
        matches = re.findall(pattern, log_content)
        parsed_logs = [{'timestamp': match[0], 'log_level': match[1], 'message': match[2]} for match in matches]
        return parsed_logs

# Django URL configuration
from django.urls import path

urlpatterns = [
    path('parse_log/', LogParserView.as_view(), name='parse-log'),
]