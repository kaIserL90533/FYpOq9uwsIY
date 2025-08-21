# 代码生成时间: 2025-08-22 06:40:50
from django.db import models
def generate_test_data():
    """
    生成测试数据的函数。
    """
    try:
        # 生成测试用户
        user = User.objects.create(username="testuser", email="test@example.com")
        # 生成测试文章
        article = Article.objects.create(title="Test Article", content="This is a test article.", author=user)
        # 生成测试评论
        comment = Comment.objects.create(content="Test comment.", article=article, author=user)
        return {"status": "success", "message": "Test data generated successfully."}
    except Exception as e:
        # 错误处理
        return {"status": "error", "message": f"Failed to generate test data: {str(e)}"}

def generate_test_users(count=10):
    """
    生成指定数量的测试用户。
    """
    for i in range(count):
        try:
            User.objects.create(username=f"testuser{i}", email=f"test{i}@example.com")
        except Exception as e:
            return {"status": "error", "message": f"Failed to create test users: {str(e)}"}
    return {"status": "success", "message": f"{count} test users generated successfully."}

def generate_test_articles(count=10):
    """
    生成指定数量的测试文章。
    """
    users = User.objects.all()
    for i in range(count):
        try:
            article = Article.objects.create(title=f"Test Article {i}", content=f"This is test article {i}.", author=users[i % len(users)])
        except Exception as e:
            return {"status": "error", "message": f"Failed to create test articles: {str(e)}"}
    return {"status": "success", "message": f"{count} test articles generated successfully."}

def generate_test_comments(count=10):
    """
    生成指定数量的测试评论。
    """
    articles = Article.objects.all()
    for i in range(count):
        try:
            comment = Comment.objects.create(content=f"Test comment {i}.", article=articles[i % len(articles)], author=User.objects.all()[i % len(User.objects.all())])
        except Exception as e:
            return {"status": "error", "message": f"Failed to create test comments: {str(e)}"}
    return {"status": "success", "message": f"{count} test comments generated successfully."}

# models.py
from django.db import models
"""
定义数据模型。
"""
class User(models.Model):
    """
    用户模型。
    """
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Article(models.Model):
    """
    文章模型。
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    评论模型。
    """
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"

# views.py
from django.http import JsonResponse
from .models import *
from .utils import *
"""
定义视图函数。
"""
def generate_data(request):
    """
    生成测试数据的视图函数。
    """
    result = generate_test_data()
    return JsonResponse(result)

def generate_users(request):
    """
    生成测试用户的视图函数。
    """
    count = int(request.GET.get("count", 10))
    result = generate_test_users(count)
    return JsonResponse(result)

def generate_articles(request):
    """
    生成测试文章的视图函数。
    """
    count = int(request.GET.get("count", 10))
    result = generate_test_articles(count)
    return JsonResponse(result)

def generate_comments(request):
    """
    生成测试评论的视图函数。
    """
    count = int(request.GET.get("count", 10))
    result = generate_test_comments(count)
    return JsonResponse(result)

# urls.py
from django.urls import path
from . import views
"""
定义URL路由。
"""
urlpatterns = [
    path("generate-data/", views.generate_data, name="generate_data"),
    path("generate-users/", views.generate_users, name="generate_users"),
    path("generate-articles/", views.generate_articles, name="generate_articles"),
    path("generate-comments/", views.generate_comments, name="generate_comments"),
]