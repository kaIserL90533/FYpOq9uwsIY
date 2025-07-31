# 代码生成时间: 2025-07-31 23:02:56
from django.db import migrations, models
a
"""
数据库迁移工具组件
"""
def create_initial_migration(app_label, model_name):
    """
    创建初始迁移文件
    
    Args:
        app_label (str): 应用标签
        model_name (str): 模型名称
    """
    # 生成迁移文件路径
    migration_file_path = f"{app_label}/migrations/0001_initial.py"
    
    # 创建迁移文件
    with open(migration_file_path, 'w') as f:
        # 编写迁移文件内容
        f.write("""# -*- coding: utf-8 -*-
"""
        f.write("""from django.db import migrations, models
"""
        f.write(f'
def create_{model_name.lower()}_initial(apps, schema_editor):
            """
            创建{model_name}表
            """
            """
            return
        f.write(f'
def reverse_{model_name.lower()}_initial(apps, schema_editor):
            """
            删除{model_name}表
            """
            """
            return
        f.write(f'class Migration(migrations.Migration):
            """
            {model_name}表初始迁移
            """
            initial = True
            dependencies = []
            operations = [
                migrations.CreateModel(
                    name=\'{model_name}\',
                    fields=[
                    ],
                ),
            ]
""")
    
    print(f"迁移文件{migration_file_path}创建成功")


def apply_migration(app_label, migration_file_path):
    """
    应用迁移
    
    Args:
        app_label (str): 应用标签
        migration_file_path (str): 迁移文件路径
    """
    try:
        # 导入迁移文件
        migration_module = __import__(f"{app_label}.migrations.{migration_file_path}", fromlist=[migration_file_path])
        
        # 应用迁移
        migration = migration_module.Migration(
            "apply",
            migration_module.Migration("dependencies", []),
        )
        migration.apply(None, None)
        print(f"迁移文件{migration_file_path}应用成功")
    except Exception as e:
        print(f"迁移文件{migration_file_path}应用失败: {e}")


def rollback_migration(app_label, migration_file_path):
    """
    回滚迁移
    
    Args:
        app_label (str): 应用标签
        migration_file_path (str): 迁移文件路径
    """
    try:
        # 导入迁移文件
        migration_module = __import__(f"{app_label}.migrations.{migration_file_path}", fromlist=[migration_file_path])
        
        # 回滚迁移
        migration = migration_module.Migration(
            "unapply",
            migration_module.Migration("dependencies", []),
        )
        migration.unapply(None, None)
        print(f"迁移文件{migration_file_path}回滚成功")
    except Exception as e:
        print(f"迁移文件{migration_file_path}回滚失败: {e}")
