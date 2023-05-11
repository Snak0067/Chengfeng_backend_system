from django.urls import path

from . import views
from .modelAction import testdb, videos

urlpatterns = [
    path('uploadVideo/', videos.upload_video),
    path('test_add_user/', testdb.test_add_user),
    path('test_get_db_data/', testdb.test_get_db_data),
    path('test_update_db/', testdb.test_update_db),
    path('login/', testdb.login),
    path('video_list/', videos.get_video_list),
]
