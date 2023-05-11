# -*- coding:utf-8 -*-
# @FileName :Permission.py
# @Time :2023/5/11 10:04
# @Author :Xiaofeng
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'Chengfeng_backend_system'
        db_table = 'permission'
