# -*- coding:utf-8 -*-
# @FileName :videos.py
# @Time :2023/5/11 10:19
# @Author :Xiaofeng
import base64
import io
import json
import os
from datetime import datetime
from ..tools import videoHelper
import cv2
import ast
from PIL import Image
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Chengfeng_backend_system import settings
from Chengfeng_backend_system.models import Video, VideoForRecognition
from Chengfeng_backend_system.tools.authVerification import resolve_token
from Chengfeng_backend_system.tools.extract_whole_pose import extract_video_wholepose
from Chengfeng_backend_system.tools.response import json_response
from ..tools.prediction import prediction


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
    num_frames = vidcap.get(7)
    # 获得速率
    rate = vidcap.get(5)
    # 获得时长
    duration = num_frames * 10 // rate / 10
    # 指定帧
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    # 获取视频的宽度（单位：像素）
    width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)

    # 获取视频的高度（单位：像素）
    height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    success, image = vidcap.read()
    imag = cv2.imwrite(png_path, image)

    return num_frames, duration, width, height


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
            if item['wholePose_path'] and len(item['wholePose_path']) > 10:
                item['whole_pose_status'] = '已提取特征'
                item['show_extract_button'] = False
            else:
                item['whole_pose_status'] = '未提取特征'
                item['show_extract_button'] = True
            if item['frame_path'] and len(item['frame_path']) > 10:
                item['frame_status'] = '已分离RGB帧'
                item['show_extract_button'] = False
            else:
                item['frame_status'] = '未提取RGB帧'
                item['show_extract_button'] = True
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
    """
    更新视频
    :param request:
    :return:
    """
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
    """
    删除视频
    :param request:
    :return:
    """
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


@csrf_exempt
def video_extract_wholepose(request):
    """
    对指定的视频id的视频进行全身姿态的估计
    :param request:
    :return:
    """
    try:
        data = json.loads(request.body)
        video_id = data.get('id')
        video = Video.objects.get(id=video_id)
        video_path = video.url
        npy_path = extract_video_wholepose(video_path)
        if npy_path is not None:
            Video.objects.filter(id=video_id).update(wholePose_path=npy_path)
            return json_response(status=200, message='导出全身姿态估计成功!')
        return json_response(status=400, message='导出全身姿态估计失败!')
    except Exception as e:
        return json_response(status=403, message=str(e))


@csrf_exempt
def download_wholePose_file(request):
    """
    下载指定的视频的特征文件
    :param request:
    :return:
    """
    data = json.loads(request.body)
    video_id = data.get('id')
    video = Video.objects.get(id=video_id)
    # wholePose_path = video.wholePose_path
    wholePose_path = "E:/dataset/AUSTL/raw_data/train_data/train_labels.csv"

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    if os.path.exists(wholePose_path):
        response = HttpResponse(readFile(wholePose_path))
        return response
    else:
        return json_response(status=403, message="不存在该视频的特征文件")


@csrf_exempt
def get_video_cover(request):
    video_data = request.FILES.get('videoFile')
    videoForRecognition = VideoForRecognition()
    token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    userid = resolve_token(token)['user_id']
    if video_data:
        # 上传的视频的名称
        file_name = video_data.name
        # 上传的地址
        file_path = settings.MEDIA_ROOT + '/' + file_name
        img_path = 'D:/Code/PythonCode/Chengfeng_backend_system/Chengfeng_backend_system/data-prepare/data' \
                   '/picture_cover/' + file_name[:-4] + '_1.png'
        with open(file_path, 'wb+') as destination:
            for chunk in video_data.chunks():
                destination.write(chunk)
        # 用cv2截取第一张图片作为封面用作前端显示
        num_frames, duration, width, height = get_video_png(file_path, img_path, 1)
        # 返回文件响应
        imageInfo = {
            "frame": num_frames,
            "width": width,
            "height": height,
            "duration": duration,
            "imageUrl": videoHelper.transform_imamge_base64(img_path)
        }
        videoForRecognition.videoName = file_name
        videoForRecognition.videoPath = file_path
        videoForRecognition.videoCoverPath = img_path
        videoForRecognition.userid = userid
        videoForRecognition.shape_width = width
        videoForRecognition.shape_height = height
        videoForRecognition.duration = duration
        videoForRecognition.num_frames = num_frames
        videoForRecognition.save()
        imageInfo['videoId'] = videoForRecognition.id
        return json_response(data=imageInfo, message='获取视频封面成功！')


def read_frames_from_folder(folder_path):
    frames = []

    # 获取文件夹中所有的文件名
    file_names = os.listdir(folder_path)

    # 遍历文件名并读取图像文件
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                image_data = f.read()
                image = Image.open(io.BytesIO(image_data))
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                image_str = base64.b64encode(buffered.getvalue()).decode()
                # 将图像添加到帧列表中
                frames.append(image_str)
    return frames


@csrf_exempt
def split_video_to_frames(request):
    data = json.loads(request.body)
    video_id = data.get('id')
    video = Video.objects.get(id=video_id)
    output_folder = 'D:/Code/PythonCode/Chengfeng_backend_system/Chengfeng_backend_system/data-prepare/data/frame/'
    output_folder = os.path.join(output_folder, os.path.basename(video.url))
    os.makedirs(output_folder, exist_ok=True)
    # 打开视频文件
    vidcap = cv2.VideoCapture(video.url)
    success, image = vidcap.read()
    frame_count = 0

    while success:
        # 生成帧文件名
        frame_filename = os.path.join(output_folder, f"{os.path.basename(video.url)}_{frame_count}.jpg")

        # 保存帧为图像文件
        cv2.imwrite(frame_filename, image)

        # 读取下一帧
        success, image = vidcap.read()
        frame_count += 1

    vidcap.release()
    frames = read_frames_from_folder(output_folder)
    for i in range(len(frames)):
        frames[i] = 'data:image/jpeg;base64,' + frames[i]
    finalList = [frames[i:i + 9] for i in range(0, len(frames), 9)]
    video.frame_path = output_folder
    video.save()
    return json_response(data=finalList, message='返回视频帧！')


@csrf_exempt
def get_video_frames(request):
    data = json.loads(request.body)
    token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    userid = resolve_token(token)['user_id']
    video_id = data.get('id')
    video = Video.objects.filter(id=video_id, userid=userid).first()
    frame_folder = video.frame_path
    frames = read_frames_from_folder(frame_folder)
    for i in range(len(frames)):
        frames[i] = 'data:image/jpeg;base64,' + frames[i]
    finalList = [frames[i:i + 9] for i in range(0, len(frames), 9)]
    return json_response(data=finalList, message='返回视频帧！')


@csrf_exempt
def recognition_get_wholePose(request):
    try:
        data = json.loads(request.body)
        video_id = data.get('videoId')
        video = VideoForRecognition.objects.get(id=video_id)
        video_path = video.videoPath
        npy_path = extract_video_wholepose(video_path)
        if npy_path is not None:
            video.wholePose_path = npy_path
            video.save()
            return json_response(status=200, message='导出全身姿态估计成功!')
    except Exception:
        return json_response(status=400, message='导出全身姿态估计失败!')


@csrf_exempt
def get_recognition_video(request):
    """
    获取所有用于手语识别的视频信息
    :param videoId:
    :return:
    """
    token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    userid = resolve_token(token)['user_id']
    videoList = VideoForRecognition.objects.filter(userid=userid)
    info = {
        "videoId": [],
        "shape": [],
        "duration": [],
        "frames": [],
        "imgUrls": [],
        "sourceUrls": [],
        "active": [],
        "result": [],

    }
    for video in videoList:
        info["videoId"].append(video.id)
        info["shape"].append([video.shape_width, video.shape_height])
        info["duration"].append(video.duration)
        info["frames"].append(video.num_frames)
        info["imgUrls"].append(videoHelper.transform_imamge_base64(video.videoCoverPath))
        info["sourceUrls"].append(videoHelper.transform_video_base64(video.videoPath))
        info["active"].append(videoHelper.judge_video_provess(video))
        if video.result is not None and len(video.result) > 5:
            info["result"].append(ast.literal_eval(video.result))
        else:
            info["result"].append([])
    return json_response(status=200, data=info, message='获取视频流列表成功!')


@csrf_exempt
def delete_recognition_video(request):
    data = json.loads(request.body)
    video_id = data.get('videoId')
    video = VideoForRecognition.objects.get(id=video_id)
    video.delete()
    return json_response(status=200, message='删除视频流成功!')


@csrf_exempt
def recognition_video_to_frames(request):
    data = json.loads(request.body)
    video_id = data.get('id')
    video = VideoForRecognition.objects.get(id=video_id)
    output_folder = 'D:/Code/PythonCode/Chengfeng_backend_system/Chengfeng_backend_system/data-prepare/data/frame/'
    frame_path = videoHelper.generate_frames_bependOn_npy(video_path=video.videoPath,
                                                          npy_folder=video.wholePose_path,
                                                          out_folder=output_folder)
    video.frame_path = frame_path
    video.save()
    return json_response(message='返回视频帧！')


@csrf_exempt
def prediction_video(request):
    data = json.loads(request.body)
    video_id = data.get('id')
    video = VideoForRecognition.objects.get(id=video_id)
    top_label, prediction_result = prediction(video.frame_path)

    video.result = json.dumps(prediction_result)
    info = {
        "top_label": top_label,
        "top5_result": json.dumps(prediction_result)
    }
    video.save()
    return json_response(status=200, data=info, message='预测视频成功!')
