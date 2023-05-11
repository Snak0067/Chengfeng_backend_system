# -*- coding:utf-8 -*-
# @FileName :testdb.py
# @Time :2023/5/11 10:53
# @Author :Xiaofeng
import datetime
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Chengfeng_backend_system.models import User
from Chengfeng_backend_system.tools.authVerification import generate_token, validate_user, md5_generation
from Chengfeng_backend_system.tools.response import json_response


def test_add_user(request):
    user_add = User(username='test', password='123456', email='1244762145@qq.com',
                    created_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    user_role=4
                    )
    user_add.save()
    return HttpResponse("<p>数据添加成功！</p>")


def test_get_db_data(request):
    """
    测试获取数据库数据
    :param request: web请求
    :return: HttpResponse相应
    """
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = User.objects.all()
    # # filter相当于SQL中的WHERE，可设置条件过滤结果
    # response2 = User.objects.filter(id=1)
    # # 获取单个对象
    # response3 = User.objects.get(id=1)
    # # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    # User.objects.order_by('name')[0:2]
    # # 数据排序
    # User.objects.order_by("id")
    # # 上面的方法可以连锁使用
    # User.objects.filter(name="runoob").order_by("id")
    # 输出所有数据
    for var in list:
        response1 += var.username + " " + str(var.created_time)
    return json_response(data=response1)


def test_update_db(request):
    """
    测试修改数据库数据表
    :param request: web请求
    :return: HttpResponse
    """
    userlist = User.objects.all()
    for var in userlist:
        var.password = md5_generation(var.password)
        var.save()

    return json_response(data="修改密码成功")


# 数据库操作
def test_delete_db(request):
    # 删除id=1的数据
    test1 = User.objects.get(id=10)
    test1.delete()

    # 另外一种方式
    # Test.objects.filter(id=1).delete()

    # 删除所有数据
    # Test.objects.all().delete()

    return HttpResponse("<p>删除成功</p>")


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户名和密码
        success, userid = validate_user(username=username, password=password)
        if success:
            # 生成token并返回
            token = generate_token(userid)
            return JsonResponse({'token': token}, status=200)
        else:
            return json_response(status=401, message="User password error, verification failed")
    else:
        return json_response(status=500, message="Wrong request method, please use post for request")
