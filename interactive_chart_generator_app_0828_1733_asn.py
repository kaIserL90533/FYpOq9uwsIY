# 代码生成时间: 2025-08-28 17:33:52
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InteractiveChartGeneratorAppConfig(AppConfig):
    # 定义应用的名称
    name = 'interactive_chart_generator_app'
    verbose_name = _('Interactive Chart Generator')

    def ready(self):
        # 导入信号处理函数
        self.get_signals()

    class Signals:
        def __init__(self):
            # 在这里设置信号处理函数
            pass

# 以下是models.py文件，包含数据模型

from django.db import models

"""
定义数据模型，用于存储图表相关数据
"""
class Chart(models.Model):
    # 图表标题
    title = models.CharField(max_length=255)
    # 图表数据
    data = models.JSONField()
    # 图表创建时间
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 以下是views.py文件，包含视图逻辑

from django.shortcuts import render
from .models import Chart
from django.http import JsonResponse

"""
定义视图，处理图表的创建和显示
"""
def chart_list(request):
    # 获取所有图表的列表
    charts = Chart.objects.all()
    return render(request, 'charts/chart_list.html', {'charts': charts})

def chart_detail(request, chart_id):
    try:
        # 根据ID获取图表详情
        chart = Chart.objects.get(pk=chart_id)
        return render(request, 'charts/chart_detail.html', {'chart': chart})
    except Chart.DoesNotExist:
        # 错误处理，图表不存在时返回JSON响应
        return JsonResponse({'error': 'Chart not found'}, status=404)

# 以下是urls.py文件，定义URL路由
from django.urls import path
from . import views

"""
定义URL路由，连接视图和URL
"""
urlpatterns = [
    path('charts/', views.chart_list, name='chart_list'),
    path('chart/<int:chart_id>/', views.chart_detail, name='chart_detail'),
]
