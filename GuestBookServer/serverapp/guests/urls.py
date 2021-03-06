# Copyright Mark B. Skouson, 2019

from django.urls import path
from . import views
import os

CLOUD_TASKS = os.environ.get('CLOUD_TASKS', False)
urlpatterns = [
    # path('', views.index, name='index'),
    path(
        '<int:host_id>/<int:event_id>/<str:unique_id>/post_vid/',
        views.post_vid_uid,
        name='post_vid_uid',
    ),
    # path('', views.index, name='index'),
    path(
        '<int:host_id>/<int:event_id>/<str:unique_id>/',
        views.guest_welcome,
        name='guest_welcome',
    ),
    path(
        '<int:host_id>/<int:event_id>/<str:unique_id>/event_info/',
        views.event_info,
        name='event_info',
    ),
    path(
        'processvideo/',
        views.process_video_do_cloud_task,
        name='process_video_do_cloud_task',
    ),
]

# TODO Need to find a way to obfuscate this so an untrusted person 
# cannot guess a video_id and have the qr code and wreak havoc
if CLOUD_TASKS in ['FALSE','False', 'false','0']:
    CLOUD_TASKS = False
if CLOUD_TASKS:
    urlpatterns +=  [
        path(
            '<int:host_id>/<int:event_id>/<str:unique_id>/<int:video_id>/',
            views.process_video_create_cloud_task,
            name='process_video_create_cloud_task',
        )
    ]    
else:
    urlpatterns += [
        path(
            '<int:host_id>/<int:event_id>/<str:unique_id>/<int:video_id>/',
            views.process_video_non_cloud_task,
            name='process_video_non_cloud_task',
        ),
    ]

