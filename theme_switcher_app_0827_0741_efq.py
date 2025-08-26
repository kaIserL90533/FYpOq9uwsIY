# 代码生成时间: 2025-08-27 07:41:29
# themes/models.py"""
This module contains the Theme model, which handles theme data for the ThemeSwitcher app.
# TODO: 优化性能
"""
from django.db import models
from django.contrib.auth.models import User


class Theme(models.Model):
    """
    A model representing a theme with a name and a CSS file path.
    """
    name = models.CharField(max_length=100)
# FIXME: 处理边界情况
    css_path = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


# themes/views.py"""
This module contains views for the ThemeSwitcher app.
"""
from django.shortcuts import render, redirect
# 改进用户体验
from django.contrib.auth.decorators import login_required
from .models import Theme
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator


@login_required
def switch_theme(request):
    """
    A view to switch the user's theme.
    
    This view handles POST requests to switch the user's theme and saves the selected
    theme in the user's profile.
    """
    try:
        user_theme = request.user.profile.theme
        new_theme_id = request.POST.get('theme_id')
        new_theme = Theme.objects.get(id=new_theme_id)
        request.user.profile.theme = new_theme
        request.user.profile.save()
        messages.success(request, 'Theme successfully switched.')
# 添加错误处理
    except Theme.DoesNotExist:
        messages.error(request, 'Invalid theme selected.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('profile')

# themes/urls.py"""
This module contains URL patterns for the ThemeSwitcher app.
"""
from django.urls import path
from .views import switch_theme

app_name = 'themes'

urlpatterns = [
    path('switch/', switch_theme, name='switch_theme'),
]

# themes/admin.py"""
This module contains admin configurations for the Theme model.
"""
from django.contrib import admin
from .models import Theme

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'css_path')
    list_filter = ('name',)
    search_fields = ('name',)

# themes/apps.py"""
This module contains the configuration for the ThemeSwitcher app.
"""
from django.apps import AppConfig

class ThemeSwitcherAppConfig(AppConfig):
    name = 'themes'
    verbose_name = 'Theme Switcher'

    def ready(self):
# TODO: 优化性能
        # Signal handlers, etc.
        pass

# themes/migrations/0001_initial.py"""
This migration creates the Theme model with its fields.
"""
# 优化算法效率
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
# 增强安全性
        migrations.CreateModel(
            name='Theme',
            fields=[
# FIXME: 处理边界情况
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
# TODO: 优化性能
                ('css_path', models.CharField(max_length=255)),
            ],
        ),
    ]

# themes/templatetags/theme_tags.py"""
This module contains template tags for theme switching.
"""
from django import template
from .models import Theme

register = template.Library()
# 改进用户体验

@register.simple_tag
def current_theme_css(request):
# TODO: 优化性能
    """
    A template tag to load the CSS file of the currently selected theme.
    """
    if request.user.is_authenticated:
        try:
            theme = request.user.profile.theme
            return theme.css_path
        except Theme.DoesNotExist:
# 优化算法效率
            return ''
# 改进用户体验
    else:
        return ''