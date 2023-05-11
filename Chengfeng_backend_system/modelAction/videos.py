# -*- coding:utf-8 -*-
# @FileName :videos.py
# @Time :2023/5/11 10:19
# @Author :Xiaofeng
from Chengfeng_backend_system.models import Video
import os
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chengfeng_backend_system.settings')
    django.setup()

    videos = Video.objects.all()
    print(videos)
