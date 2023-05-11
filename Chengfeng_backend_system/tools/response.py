# -*- coding:utf-8 -*-
# @FileName :response.py
# @Time :2023/5/11 11:25
# @Author :Xiaofeng
from django.http import JsonResponse


def json_response(data=None, status=200, message=None):
    # 构建响应数据
    response_data = {'data': data}
    if message:
        response_data['message'] = message

    # 返回 JSON 格式的响应
    return JsonResponse(response_data, status=status)
