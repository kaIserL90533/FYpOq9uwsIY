# 代码生成时间: 2025-08-02 20:32:53
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.views import View

"""
用户登录验证系统组件，包含以下功能：
1. 登录页面渲染
2. 登录请求处理
3. 登录成功与失败的错误处理
"""

class LoginView(View):
    """
    用户登录视图
    """
    @require_http_methods(['GET', 'POST'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        """
        渲染登录页面
        """
        return render(request, 'login.html')
    
    def post(self, request):
        """
        处理登录请求
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # 登录成功
                login(request, user)
                return redirect('home')
            else:
                # 密码错误
                messages.error(request, '用户名或密码错误。')
        else:
            # 用户名或密码为空
            messages.error(request, '用户名和密码不能为空。')
        
        return self.get(request)

# URL配置
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]

# models.py
from django.db import models
"""
用户模型
"""
class User(models.Model):
    """
    用户模型，包含用户名、密码等基本信息
    """
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

# views.py
# 见LoginView类定义

# urls.py
# 见urlpatterns配置