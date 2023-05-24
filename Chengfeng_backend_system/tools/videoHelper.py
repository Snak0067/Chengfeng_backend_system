# -*- coding:utf-8 -*-
# @FileName :videoHelper.py
# @Time :2023/5/24 21:11
# @Author :Xiaofeng
import base64
import io
from PIL import Image


def transform_video_base64(video_path):
    # 打开视频文件并读取内容
    with open(video_path, 'rb') as video_file:
        video_content = video_file.read()

    # 将视频内容编码为Base64字符串
    video_base64 = base64.b64encode(video_content).decode()

    return "data:video/mp4;base64," + video_base64


def transform_imamge_base64(img_path):
    with open(img_path, 'rb') as f:
        image_data = f.read()
        image = Image.open(io.BytesIO(image_data))
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_str = base64.b64encode(buffered.getvalue()).decode()
        return 'data:image/jpeg;base64,' + image_str


