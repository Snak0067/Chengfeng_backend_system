# -*- coding:utf-8 -*-
# @FileName :User.py
# @Time :2023/5/11 9:58
# @Author :Xiaofeng
from django.db import models


class User(models.Model):
    # IntegerField 是 Django 中的一个模型字段类型，它用于表示整数类型的数据库字段
    # IntegerField 类接受一些可选参数，例如 null 和 blank，用于控制该字段是否可以为空
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_time = models.DateTimeField()
    user_role = models.IntegerField()

    class Meta:
        app_label = 'Chengfeng_backend_system'
        db_table = 'users'
