from django.urls import path

from . import views

urlpatterns = [
    path('uploadVideo/', views.upload_video),
]
