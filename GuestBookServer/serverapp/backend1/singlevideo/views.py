from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
import os
import string
import random
from datetime import datetime, timedelta
import ffmpeg
from singlevideo.apps import create_standard_thumb_mini_videos
from google.cloud import storage
from google.protobuf import timestamp_pb2
import json
from google.cloud import tasks_v2
import io
import time


@csrf_exempt
def index(request):
    context = {}
    return render(request, 'home/index.html', context)


# Create your views here.

@csrf_exempt
def process_video_do_cloud_task(request):
    """
    (Part 2 of cloud task version of process video)
    This is the routine cloud tasks will call to 
    process the video.
    This will call the routine to process the video.
    return: The status of the request through a JsonResponse
    """
    print('in process_video_do_cloud_task')
    context = {}
    body = json.loads(request.body.decode())
    print(body['infname'])
    create_standard_thumb_mini_videos(
         body['infname'], 
         body['processedfname'],
         body['thumbfname'],
         body['mfname'],
    )
    context['return_status'] = 'successfully processed'
    return JsonResponse(context)

