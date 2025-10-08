# 代码生成时间: 2025-10-08 18:23:45
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

"""
定义一个模型，用于存储提交的作业和自动批改结果。
"""
class Assignment(models.Model):
    """
    作业模型，存储作业的名称、提交截止日期和相关描述。
    """
    name = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Assignments"

class Submission(models.Model):
    """
    提交模型，存储学生的提交内容和与作业的关联。
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    score = models.IntegerField(blank=True, null=True)  # 分数
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.submitted_at}"

    def clean(self):
        """
        校验提交的代码长度，确保其在合理范围内。
        """
        if len(self.code) > 10000:  # 假设代码长度上限为10000字符
            raise ValidationError("提交的代码过长。")

# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Assignment, Submission
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

"""
定义视图，处理作业的提交和自动批改。
"""
@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def submit_assignment(request, assignment_id):
    """
    提交作业的视图，接受学生提交的代码并保存。
    """
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        submission = Submission(
            assignment=assignment,
            student=request.user,
            code=request.POST.get('code')
        )
        submission.clean()  # 校验代码长度
        submission.save()
        return HttpResponse("提交成功。")
    else:
        return render(request, 'submit_assignment.html', {'assignment': assignment})

# urls.py
from django.urls import path
from . import views

"""
URL配置，定义应用的路由。
"""
urlpatterns = [
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
]