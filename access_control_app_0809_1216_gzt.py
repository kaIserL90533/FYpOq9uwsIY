# 代码生成时间: 2025-08-09 12:16:41
{
        "filename": "permissions\models.py",
        "code": """# permissions\models.py
        # Django model for access control

        from django.db import models

        class User(models.Model):
            username = models.CharField(max_length=100)
            is_active = models.BooleanField(default=True)

            def __str__(self):
                return self.username

        """
