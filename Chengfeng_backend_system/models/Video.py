# -*- coding:utf-8 -*-
# @FileName :Video.py
# @Time :2023/5/11 9:57
# @Author :Xiaofeng
from django.db import models


class Video(models.Model):
    userid = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255)
    result = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        app_label = 'Chengfeng_backend_system'
        db_table = 'videos'
