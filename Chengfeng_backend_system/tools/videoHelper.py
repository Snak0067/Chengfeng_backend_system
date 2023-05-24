# -*- coding:utf-8 -*-
# @FileName :videoHelper.py
# @Time :2023/5/24 21:11
# @Author :Xiaofeng
import base64
import io
from PIL import Image
import os
import subprocess


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


def judge_video_provess(video):
    active = 0
    if video.wholePose_path is not None and len(video.wholePose_path) > 5:
        active = 1
        if video.frame_path is not None and len(video.frame_path) > 5:
            active = 2
            if video.result is not None:
                active = 3
    return active


def batch_convert_videos(input_dir, output_dir):
    # 获取文件夹中所有的文件名
    file_names = os.listdir(input_dir)
    # 遍历文件名并读取图像文件
    for file_name in file_names:
        file_path = os.path.join(input_dir, file_name)
        # 构建FFmpeg命令
        ffmpeg_cmd = f'ffmpeg -i {file_path} -vcodec h264 {file_name}'
        # 执行FFmpeg命令
        subprocess.call(ffmpeg_cmd, shell=True)


def video_transcoding():
    # 设置输入目录和输出目录
    input_directory = "D:/Code/PythonCode/SignLanguageProject/videoMaterials/input/"
    output_directory = "D:/Code/PythonCode/SignLanguageProject/videoMaterials/output/"

    # 执行批量转码
    batch_convert_videos(input_directory, output_directory)


if __name__ == '__main__':
    video_transcoding()
