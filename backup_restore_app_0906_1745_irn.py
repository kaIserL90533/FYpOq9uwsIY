# 代码生成时间: 2025-09-06 17:45:49
 * 添加了docstrings和注释，以及错误处理。
 */

import os
import shutil
import datetime
from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from django.conf import settings
from django.core.management import call_command

# 数据备份模型
class BackupModel:
    """
    负责数据备份的操作。
    """
    def __init__(self):
        self.backup_dir = os.path.join(settings.BASE_DIR, 'backup')
        self.today = datetime.date.today()
        self.backup_path = os.path.join(self.backup_dir, f"backup_{self.today}.sql")
        self.conn = None

    def backup_database(self):
        """
        备份数据库。
        """
        try:
            self.conn = connections[DEFAULT_DB_ALIAS]
            with open(self.backup_path, 'w') as f:
                call_command('dumpdata', output=f, stdout=None)
                call_command('sqlsequencereset', self.conn.alias, stdout=f)
                # 导出数据库结构
                with self.conn.cursor() as cursor:
                    cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
                    cursor.execute('SET SQL_LOG_BIN=0;')
                    cursor.execute('SELECT CONCAT("DROP TABLE IF EXISTS `", table_name, "`;") INTO @s FROM information_schema.tables WHERE table_schema="{db}";'.format(db=self.conn.settings_dict['NAME']))
                    cursor.execute('SET @s = CONCAT(@s, "DROP TABLE IF EXISTS `information_schema.COLUMNS`;");')
                    cursor.execute('PREPARE s FROM @s; EXECUTE s; DEALLOCATE PREPARE s;')
                    cursor.execute('SET SQL_LOG_BIN=1;')
                    cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
                    cursor.execute('SELECT CONCAT("CREATE TABLE `", table_name, "` (") INTO @s FROM information_schema.tables WHERE table_schema="{db}";'.format(db=self.conn.settings_dict['NAME']))
                    cursor.execute('SET @s = CONCAT(@s, ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")')
                    cursor.execute('PREPARE s FROM @s; EXECUTE s; DEALLOCATE PREPARE s;')
                    cursor.execute('SELECT CONCAT("INSERT INTO `", table_name, "` VALUES ") INTO @s FROM information_schema.tables WHERE table_schema="{db}";'.format(db=self.conn.settings_dict['NAME']))
                    cursor.execute('SET @s = CONCAT(@s, "SELECT * FROM `{db}`.`", table_name, "`;")')
                    cursor.execute('PREPARE s FROM @s; EXECUTE s; DEALLOCATE PREPARE s;')
            print(f"数据库备份成功，备份文件路径为：{self.backup_path}")
        except Exception as e:
            print(f"数据库备份失败，错误信息：{e}")

    def restore_database(self, backup_file):
        """
        恢复数据库。
        """
        try:
            with open(backup_file, 'r') as f:
                call_command('loaddata', f, stdout=None)
            print(f"数据库恢复成功，恢复文件路径为：{backup_file}")
        except Exception as e:
            print(f"数据库恢复失败，错误信息：{e}")

# 数据备份恢复视图
def backup_restore_view(request):
    """
    数据备份恢复视图。
    """
    if request.method == 'POST':
        backup_model = BackupModel()
        if request.POST.get('action') == 'backup':
            backup_model.backup_database()
        elif request.POST.get('action') == 'restore':
            backup_file = request.POST.get('backup_file')
            backup_model.restore_database(backup_file)
        return HttpResponse('操作成功')
    else:
        return HttpResponse('不支持的请求方法', status=405)

# 数据备份恢复URL配置
urlpatterns = [
    path('backup_restore/', backup_restore_view, name='backup_restore'),
]
