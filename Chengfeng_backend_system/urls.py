from django.urls import path

from .modelAction import testdb, videos

urlpatterns = [
    path('uploadVideo/', videos.upload_video),
    path('test_add_user/', testdb.test_add_user),
    path('test_get_db_data/', testdb.test_get_db_data),
    path('test_update_db/', testdb.test_update_db),
    path('login/', testdb.login),
    path('video_list/', videos.get_video_list),
    path('update_video/', videos.update_video),
    path('delete_video/', videos.delete_video),
    path('extract_wholepose/', videos.video_extract_wholepose),
    path('download_wholePose_file/', videos.download_wholePose_file),
    path('get_video_cover/', videos.get_video_cover),
    path('split_video_to_frames/', videos.split_video_to_frames),
    path('get_video_frames/', videos.get_video_frames),
    path('recognition_get_wholePose/', videos.recognition_get_wholePose),
    path('getAllVideoInfo/', videos.get_recognition_video),
    path('delete_recognition_video/', videos.delete_recognition_video),
    path('recognition_video_to_frames/', videos.recognition_video_to_frames),

]
