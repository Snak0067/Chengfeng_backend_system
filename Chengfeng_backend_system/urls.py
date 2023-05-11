from django.urls import path

from . import views
from . import testdb

urlpatterns = [
    path('uploadVideo/', views.upload_video),
    path('test_add_user/', testdb.test_add_user),
    path('test_get_db_data/', testdb.test_get_db_data),
]
