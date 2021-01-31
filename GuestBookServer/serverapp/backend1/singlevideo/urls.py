# Copyright Mark B. Skouson, 2019

from django.urls import path
from . import views
import os

CLOUD_TASKS = os.environ.get('CLOUD_TASKS', False)
urlpatterns = [
    path('', views.index, name='index'),
    path(
        'processvideo/',
        views.process_video_do_cloud_task,
        name='process_video_do_cloud_task',
    ),
]

