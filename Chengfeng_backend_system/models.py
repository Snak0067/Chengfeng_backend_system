# -*- coding:utf-8 -*-
# @FileName :models.py.py
# @Time :2023/5/11 10:26
# @Author :Xiaofeng

from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)


class Video(models.Model):
    userid = models.IntegerField()
    title = models.CharField(max_length=255)
    videoName = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255)
    result = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    img = models.CharField(max_length=255, null=True, blank=True)
    videoType = models.CharField(max_length=255)
    wholePose_path = models.CharField(max_length=255, null=True, blank=True)
    feature_path = models.CharField(max_length=255, null=True, blank=True)
    frame_path = models.CharField(max_length=255, null=True, blank=True)


class VideoForRecognition(models.Model):
    userid = models.IntegerField()
    videoName = models.CharField(max_length=255)
    videoPath = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    shape_width = models.CharField(max_length=255, default=244)
    shape_height = models.CharField(max_length=255, default=168)
    duration = models.FloatField(default=2.0)
    num_frames = models.IntegerField(default=64)
    videoCoverPath = models.CharField(max_length=255, null=True, blank=True)
    frame_path = models.CharField(max_length=255, null=True, blank=True)
    wholePose_path = models.CharField(max_length=255, null=True, blank=True)
    feature_path = models.CharField(max_length=255, null=True, blank=True)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)


class User(models.Model):
    # IntegerField 是 Django 中的一个模型字段类型，它用于表示整数类型的数据库字段
    # IntegerField 类接受一些可选参数，例如 null 和 blank，用于控制该字段是否可以为空
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_time = models.DateTimeField()
    user_role = models.IntegerField()
