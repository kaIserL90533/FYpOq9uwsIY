# 代码生成时间: 2025-09-18 17:23:11
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
import random
import string
import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class TestData(models.Model):
    """测试数据模型"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# Views
class GenerateTestData(View):
    """测试数据生成器视图"""
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        "