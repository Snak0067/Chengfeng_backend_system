# -*- coding:utf-8 -*-
# @FileName :views.py
# @Time :2023/5/8 16:35
# @Author :Xiaofeng
from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_video(request):
    """
    使用@csrf_exempt装饰器来禁用CSRF保护。由于在上传大型文件时，可能会超出Django默认的文件大小限制，
    因此需要设置DATA_UPLOAD_MAX_MEMORY_SIZE和FILE_UPLOAD_MAX_MEMORY_SIZE来增加Django对大型文件的支持
    :param request:
    :return:
    """
    if request.method == 'POST':
        video_file = request.FILES.get('file')
        if video_file:
            file_name = video_file.name
            file_path = settings.MEDIA_ROOT + '/' + file_name
            with open(file_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            return JsonResponse({'status': 'success', 'file_path': file_path})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

