# 代码生成时间: 2025-08-30 15:50:28
import os
from django.db import models
from django.http import JsonResponse
from django.views import View
from PIL import Image
from io import BytesIO

"""
图片尺寸批量调整器应用组件
"""

# 应用组件配置
APP_DIR = os.path.dirname(os.path.abspath(__file__))


class ImageDimensionAdjuster(models.Model):
    """
    图片尺寸调整记录
    """
    image = models.ImageField(upload_to='images')
    original_width = models.IntegerField()
    original_height = models.IntegerField()
    target_width = models.IntegerField()
    target_height = models.IntegerField()
    adjusted_image = models.ImageField(upload_to='adjusted_images', null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        保存图片前进行尺寸调整
        """
        if self.image:
            image = Image.open(self.image)
            self.original_width, self.original_height = image.size
            self.adjusted_image = self.adjust_dimension(image)
        super().save(*args, **kwargs)

    def adjust_dimension(self, image):
        """
        调整图片尺寸
        """
        buffer = BytesIO()
        image = image.resize((self.target_width, self.target_height), Image.ANTIALIAS)
        image.save(buffer, format=image.format)
        buffer.seek(0)
        new_image = Image.open(buffer)
        return new_image

    def __str__(self):
        return f'{self.image} resized to {self.target_width}x{self.target_height}'


class AdjustImageDimensionView(View):
    """
    视图：批量调整图片尺寸
    """
    def post(self, request):
        """
        通过POST请求接收图片和尺寸参数，调整图片尺寸
        """
        try:
            image = request.FILES.get('image')
            target_width = int(request.POST.get('target_width'))
            target_height = int(request.POST.get('target_height'))
            
            if not image:
                return JsonResponse({'error': 'No image provided.'}, status=400)
            
            image_model = ImageDimensionAdjuster(
                image=image,
                target_width=target_width,
                target_height=target_height
            )
            image_model.save()
            return JsonResponse({'message': 'Image resized successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# urls.py
# from django.urls import path
# from .views import AdjustImageDimensionView

# urlpatterns = [
#     path('adjust-image/', AdjustImageDimensionView.as_view(), name='adjust_image_dimension'),
# ]