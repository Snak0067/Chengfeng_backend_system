# -*- coding:utf-8 -*-
# @FileName :videos.py
# @Time :2023/5/11 10:19
# @Author :Xiaofeng
import json
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

from Chengfeng_backend_system import settings
from Chengfeng_backend_system.models import Video
from Chengfeng_backend_system.tools.authVerification import resolve_token
from Chengfeng_backend_system.tools.response import json_response


@csrf_exempt
def get_video_list(request):
    """
    获取token解析出来的用户的所有视频信息
    """
    if request.method == 'POST':
        # 获取用户名和密码
        data = json.loads(request.body.decode('utf-8'))
        token = request.POST.get('token')
        userid = resolve_token(token)['user_id']
        videolist = Video.objects.get(userid=userid)

        #
        #     return json_response(data=responseData, status=200, message="登录成功！")
        # else:
        #     return json_response(status=401, message="用户密码错误，验证失败！")
    else:
        return json_response(status=500, message="请求方式错误，请使用post请求！")


@csrf_exempt
def upload_video(request):
    """
    上传视频
    """
    try:
        if request.method == 'POST':
            video = Video()
            video_file_data = request.FILES.get('videoFile')
            video.title = request.POST.get('videoName')
            video.description = request.POST.get('videoDescribe')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            video.create_time = current_time
            video.update_time = current_time
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            video.userid = resolve_token(token)['user_id']
            if video_file_data:
                file_name = video_file_data.name
                file_path = settings.MEDIA_ROOT + '/' + file_name
                video.url = file_path
                with open(file_path, 'wb+') as destination:
                    for chunk in video_file_data.chunks():
                        destination.write(chunk)
                video.save()
                return json_response(status=200, message='上传成功')
    except Exception as e:
        return json_response(status=400, message=str(e))
    return json_response(status=400, message='上传失败!')
