# -*- coding:utf-8 -*-
# @FileName :Role.py
# @Time :2023/5/11 10:03
# @Author :Xiaofeng
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'Chengfeng_backend_system'
        db_table = 'role'
