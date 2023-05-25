# -*- coding:utf-8 -*-
# @FileName :prediction.py
# @Time :2023/5/24 23:48
# @Author :Xiaofeng
import os
from collections import OrderedDict
from random import random

import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image, ImageOps

from models.Conv3D import r2plus1d_18

# Hyperparams
num_classes = 226  # 100
epochs = 100
# batch_size = 16
test_clips = 5
batch_size = 24
learning_rate = 1e-5  # 1e-4 Train 1e-5 Finetune
log_interval = 80
sample_size = 128
sample_duration = 32
attention = False
drop_p = 0.0
hidden1, hidden2 = 512, 256
num_workers = 12
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([transforms.Resize([sample_size, sample_size]),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.5], std=[0.5])])


def get_video_item(images_path):
    images = []
    for i in range(test_clips):
        images.append(read_images(images_path, i))
    images = torch.stack(images, dim=0)
    return images


def read_images(folder_path, clip_no=0):
    # assert len(os.listdir(folder_path)) >= self.frames, "Too few images in your data folder: " + str(folder_path)
    images = []
    index_list = frame_indices_tranform_test(len(os.listdir(folder_path)), sample_duration, clip_no)

    for i in index_list:
        try:
            image_path = folder_path + '/' + '{:04d}.jpg'.format(i)
            image = Image.open(image_path)

        except FileNotFoundError:
            print(f'image does not find {image_path}')
            continue
        crop_box = (16, 16, 240, 240)
        image = image.crop(crop_box)
        # assert image.size[0] == 224
        image = transform(image)

        images.append(image)

    images = torch.stack(images, dim=0)
    # switch dimension for 3d cnn
    images = images.permute(1, 0, 2, 3)
    # print(images.shape)
    return images


def frame_indices_tranform_test(video_length, sample_duration, clip_no=0):
    # 如果视频长度大于采样时长（sample_duration），则根据剪辑编号（clip_no）计算起始帧索引。
    if video_length > sample_duration:
        start = (video_length - sample_duration) // (test_clips - 1) * clip_no
        frame_indices = np.arange(start, start + sample_duration) + 1
    # 如果视频长度等于采样时长，则直接生成从1到采样时长的连续帧索引。
    elif video_length == sample_duration:
        frame_indices = np.arange(sample_duration) + 1
    # 如果视频长度小于采样时长，则通过将视频中的帧索引循环连接，直到满足采样时长的要求。
    # 然后，从生成的帧索引中选择前采样时长个帧索引。
    else:
        frame_indices = np.arange(video_length)
        while frame_indices.shape[0] < sample_duration:
            frame_indices = np.concatenate((frame_indices, np.arange(video_length)), axis=0)
        frame_indices = frame_indices[:sample_duration] + 1

    return frame_indices


def prediction(video_path):
    inputs_clips = get_video_item(video_path)
    model = r2plus1d_18(pretrained=True, num_classes=226)
    # load pretrained
    checkpoint = torch.load('checkpoints/sign_resnet2d+1_epoch099.pth')
    new_state_dict = OrderedDict()
    for k, v in checkpoint.items():
        name = k[7:]  # remove 'module.'
        new_state_dict[name] = v
    model.load_state_dict(new_state_dict)
    model = model.to(device)
    model = nn.DataParallel(model)
    # prediction
    outputs_clips = []
    for i_clip in range(inputs_clips.size(1)):
        inputs = inputs_clips[:, i_clip, :, :]
        outputs_clips.append(model(inputs))
    outputs = torch.mean(torch.stack(outputs_clips, dim=0), dim=0)
    # collect labels & prediction
    prediction = torch.max(outputs, 1)[1]
    score_frag = outputs.data.cpu().numpy()
    score = np.concatenate(score_frag)

    print(prediction, score_frag, score)
    return prediction


if __name__ == '__main__':
    video_path = "D:/Code/PythonCode/Chengfeng_backend_system/Chengfeng_backend_system/data-prepare/data/frame/05234" \
                 ".mp4"
    prediction(video_path)
