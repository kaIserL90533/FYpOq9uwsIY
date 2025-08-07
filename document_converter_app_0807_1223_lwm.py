# 代码生成时间: 2025-08-07 12:23:42
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.urls import path
import os
import docx2txt
import pdf2docx


# 定义一个错误处理类
class ConverterError(Exception):
    pass


# 创建一个文档格式转换器的视图
class DocumentConverterView(View):
    """
    视图类用于处理文档格式的转换。
    
    允许用户上传文档，并将其转换为指定的格式。
    """
    def get(self, request):
        # 渲染上传页面
        return render(request, 'upload.html')
    
    def post(self, request):
        """
        处理POST请求，将上传的文档从一种格式转换为另一种格式。
        
        :param request: 包含上传文件的HTTP请求对象。
        :return: JSON响应，包含转换结果或错误信息。
        """
        file = request.FILES.get('document')
        if not file:
            raise ConverterError('No document provided.')
        
        try:
            # 检查文件格式并进行相应的转换
            if file.name.endswith('.docx'):
                text = docx2txt.process(file)
                return JsonResponse({'message': 'Document converted successfully.', 'text': text})
            elif file.name.endswith('.pdf'):
                docx_file = pdf2docx.convert(file)
                return JsonResponse({'message': 'PDF converted to DOCX successfully.', 'docx': docx_file})
            else:
                raise ConverterError('Unsupported file format.')
        except ConverterError as ce:
            # 捕获转换错误并返回错误信息
            return JsonResponse({'error': str(ce)}, status=400)
        except Exception as e:
            # 捕获其他异常并返回错误信息
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


# 定义URL模式
urlpatterns = [
    path('convert/', DocumentConverterView.as_view(), name='document-converter'),
]


# 定义models.py，用于存储转换后的文档信息，如果需要
# 因为我们不处理文件存储，所以这里留空
# models.py
# from django.db import models

# class ConvertedDocument(models.Model):
#     """
#    模型类用于存储转换后的文档信息。
#     """
#     file = models.FileField(upload_to='converted_documents/')
#     date_converted = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f'{self.file} converted on {self.date_converted}'
