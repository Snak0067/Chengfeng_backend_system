# -*- coding:utf-8 -*-
# @FileName :videoHelper.py
# @Time :2023/5/24 21:11
# @Author :Xiaofeng
import base64
import io

import cv2
import numpy as np
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
            if video.result is not None and len(video.result) > 2:
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


selected_joints = np.concatenate(([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                  [91, 95, 96, 99, 100, 103, 104, 107, 108, 111],
                                  [112, 116, 117, 120, 121, 124, 125, 128, 129, 132]), axis=0)


def crop(image, center, radius, size=512):
    scale = 1.3
    radius_crop = (radius * scale).astype(np.int32)
    center_crop = (center).astype(np.int32)

    rect = (max(0, (center_crop - radius_crop)[0]), max(0, (center_crop - radius_crop)[1]),
            min(512, (center_crop + radius_crop)[0]), min(512, (center_crop + radius_crop)[1]))

    image = image[rect[1]:rect[3], rect[0]:rect[2], :]

    if image.shape[0] < image.shape[1]:
        top = abs(image.shape[0] - image.shape[1]) // 2
        bottom = abs(image.shape[0] - image.shape[1]) - top
        image = cv2.copyMakeBorder(image, top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    elif image.shape[0] > image.shape[1]:
        left = abs(image.shape[0] - image.shape[1]) // 2
        right = abs(image.shape[0] - image.shape[1]) - left
        image = cv2.copyMakeBorder(image, 0, 0, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return image


def generate_frames_bependOn_npy(video_path, npy_folder, out_folder):
    name = os.path.basename(video_path)
    print(name)
    cap = cv2.VideoCapture(video_path)
    npy = np.load(npy_folder).astype(np.float32)
    npy = npy[:, selected_joints, :2]
    npy[:, :, 0] = 512 - npy[:, :, 0]
    xy_max = npy.max(axis=1, keepdims=False).max(axis=0, keepdims=False)
    xy_min = npy.min(axis=1, keepdims=False).min(axis=0, keepdims=False)
    assert xy_max.shape == (2,)
    xy_center = (xy_max + xy_min) / 2 - 20
    xy_radius = (xy_max - xy_center).max(axis=0)
    index = 0
    while True:
        ret, frame = cap.read()
        if ret:
            image = crop(frame, xy_center, xy_radius)
        else:
            break
        index = index + 1
        image = cv2.resize(image, (256, 256))

        frame_path = os.path.join(out_folder, name[:-4])
        if not os.path.exists(frame_path):
            os.makedirs(frame_path)
        cv2.imwrite(os.path.join(frame_path, '{:04d}.jpg'.format(index)), image)
    return frame_path


if __name__ == '__main__':
    video_transcoding()
