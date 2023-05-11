# -*- coding:utf-8 -*-
# @FileName :testdb.py
# @Time :2023/5/11 10:53
# @Author :Xiaofeng
import datetime
import time

from django.http import HttpResponse

from Chengfeng_backend_system.models import User


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
    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = User.objects.filter(id=1)
    # 获取单个对象
    response3 = User.objects.get(id=1)
    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    User.objects.order_by('name')[0:2]
    # 数据排序
    User.objects.order_by("id")
    # 上面的方法可以连锁使用
    User.objects.filter(name="runoob").order_by("id")
    # 输出所有数据
    for var in list:
        response1 += var.username + " " + str(var.created_time)
    response = response1
    return HttpResponse("<p>" + response + "</p>")


def test_update_db(request):
    """
    测试修改数据库数据表
    :param request: web请求
    :return: HttpResponse
    """
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = User.objects.get(id=1)
    test1.name = 'Google'
    test1.save()

    # 另外一种方式
    # Test.objects.filter(id=1).update(name='Google')

    # 修改所有的列
    # Test.objects.all().update(name='Google')

    return HttpResponse("<p>修改成功</p>")


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
