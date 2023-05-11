# -*- coding:utf-8 -*-
# @FileName :authVerification.py
# @Time :2023/5/11 12:49
# @Author :Xiaofeng
from Chengfeng_backend_system.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import jwt
import hashlib

secret_key = 'Chengfeng_backend_system'


def generate_token(userid):
    """
    使用jwt库生成JWT token，可以自行安装并引入。
    secret_key需要自行设置为一个安全的随机字符串。在其他需要登录验证的API中可以使用jwt库验证token是否有效
    :param user:
    :return:
    """

    # 设置token有效期为30分钟
    exp_time = datetime.utcnow() + timedelta(hours=30)
    payload = {
        'user_id': userid,
        'exp': exp_time
    }
    # 生成token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def resolve_token(token):
    # 解码token
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    return decoded_token


def md5_generation(encrypted_string):
    # 创建 MD5 对象
    md5 = hashlib.md5()
    # 将字符串转为二进制，并使用 update 方法更新 MD5 对象
    md5.update(encrypted_string.encode('utf-8'))
    # 获取加密后的结果
    encrypted_password = md5.hexdigest()
    return encrypted_password


def validate_user(username, password):
    """
    根据用户名查询 User 模型，
    1、如果存在则调用 check_password() 方法判断密码是否匹配。
    2、如果用户名不存在或密码不匹配则返回 False，否则返回 True
    :param username: 用户名
    :param password: 密码
    :return:
    """
    try:
        user = User.objects.get(username=username)
        if md5_generation(password) == user.password:
            return True, user.id
        else:
            return False, None
    except User.DoesNotExist:
        return False, None
