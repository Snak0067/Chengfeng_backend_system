# -*- coding:utf-8 -*-
# @FileName :videos.py
# @Time :2023/5/11 10:19
# @Author :Xiaofeng
import json
from datetime import datetime
from PIL import Image
import base64
import io
import cv2
from django.views.decorators.csrf import csrf_exempt

from Chengfeng_backend_system import settings
from Chengfeng_backend_system.models import Video
from Chengfeng_backend_system.tools.authVerification import resolve_token
from Chengfeng_backend_system.tools.response import json_response


def get_video_png(video_path, png_path, zhen_num=1):
    """
    获取视频封面
    :param video_path: 视频文件路径
    :param png_path: 截取图片存储路径
    :param zhen_num: 指定截取视频第几帧
    :return:
    """
    vidcap = cv2.VideoCapture(video_path)
    # 获取帧数
    zhen_count = vidcap.get(7)

    if zhen_num > zhen_count:
        zhen_num = 1
    print(f"zhen_count = {zhen_count} | last zhen_num = {zhen_num}")

    # 指定帧
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, zhen_num)

    success, image = vidcap.read()
    imag = cv2.imwrite(png_path, image)


@csrf_exempt
def get_video_list(request):
    """
    获取token解析出来的用户的所有视频信息
    """

    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        userid = resolve_token(token)['user_id']

        # 获取需要筛选的数据信息
        body_data = json.loads(request.body.decode('utf-8'))
        sort_videoName = body_data.get('title', '')  # 如果没有title，则默认为空字符串
        sort_videoType = body_data.get('type', '')  # 如果没有type，则默认为空字符串
        sort_order = body_data.get('sort', 'id')
        if sort_order == '+id':
            sort_order = 'id'
        videolist = Video.objects.filter(userid=userid)

        if sort_videoName:
            videolist = videolist.filter(videoName=sort_videoName)
        if sort_videoType:
            videolist = videolist.filter(videoType=sort_videoType)

        videolist = list(videolist.order_by(sort_order).values())

        for item in videolist:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            img_path = item['img']
            with open(img_path, 'rb') as f:
                image_data = f.read()
                image = Image.open(io.BytesIO(image_data))
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                image_str = base64.b64encode(buffered.getvalue()).decode()
                item['img'] = image_str
            if item['wholePose_path'] is not None:
                item['status'] = '已完成'
            else:
                item['status'] = '未提取特征'
        responseData = {'videolist': videolist}
        return json_response(data=responseData, status=200, message="获取视频列表成功！")
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
            video.videoType = str(request.POST.get('videoType'))
            video.description = request.POST.get('videoDescribe')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            video.create_time = current_time
            video.update_time = current_time
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            video.userid = resolve_token(token)['user_id']
            if video_file_data:
                # 上传的视频的名称
                file_name = video_file_data.name
                video.videoName = file_name
                # 上传的地址
                file_path = settings.MEDIA_ROOT + '/' + file_name
                img_path = 'D:/Code/PythonCode/Chengfeng_backend_system/Chengfeng_backend_system/data-prepare/data' \
                           '/picture_cover/' + file_name[:-4] + '_1.png'

                with open(file_path, 'wb+') as destination:
                    for chunk in video_file_data.chunks():
                        destination.write(chunk)
                video.url = file_path
                # 用cv2截取第一张图片作为封面用作前端显示
                get_video_png(file_path, img_path, 1)
                video.img = img_path

                video.save()

                return json_response(status=200, message='上传成功')
    except Exception as e:
        return json_response(status=400, message=str(e))
    return json_response(status=400, message='上传失败!')


@csrf_exempt
def update_video(request):
    data = json.loads(request.body)
    video_id = data.get('id')
    if video_id:
        video = Video.objects.filter(id=video_id)
        if video:
            video.update(
                title=data.get('title'),
                videoName=data.get('videoName'),
                videoType=data.get('videoType'),
                description=data.get('description'),
            )
            return json_response(status=200, message='更新视频数据成功')
    return json_response(status=400, message='更新数据失败!')


@csrf_exempt
def delete_video(request):
    data = json.loads(request.body)
    video_id = data.get('id')
    if video_id:
        try:
            video = Video.objects.get(id=video_id)
            video.delete()
            return json_response(status=200, message='删除成功!')

        except Video.DoesNotExist:
            return json_response(status=403, message='视频不存在!')
    else:
        return json_response(status=403, message='Video ID is required!')
