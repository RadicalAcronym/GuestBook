from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from hosts.models import User, Event
import os
import string
import random
from datetime import datetime, timedelta
import ffmpeg
from guests.apps import create_standard_thumb_mini_videos
from google.cloud import storage
from google.protobuf import timestamp_pb2
import json
from google.cloud import tasks_v2
import io
import time


# Create your views here.

@csrf_exempt
def post_vid_uid(request, host_id, event_id, unique_id):
    """
    This is the initial handler of a request from 
    a guest to post a video.
    It will 
      - Check to make sure the unique ID matches 
        the host and event
      - Create a URL for the guest to post directly
        to the google cloud storage location
      - Add an entry to the database for this video
    :return:
      the direct site URL and the video id to the
      guest through a JsonResponse

    The process is as follows (assuming the guest has the app and the right URL)
    - Assume the Guest gets a url from a QR code
    - The guest initiates a post to send the guest's name to Server
    - Server uses guestsname to create a gcloud direct URL and sends that and 
      the video id to the guest
    - Guest then uploads the video to the gcloud url, and uses the video id to 
      generate the success redirect url.  
    - If the gcloud upload request is successful Guest is redirected to the 
      success_action_redirect Guest created.
    - When Server sees Guest go to the success_action_redirect site, it creates a 
      google task to process the video to standardize format, and create a 
      smaller version and a thumbnail picture.
    - Once the google procesing task is kicked off, the Server returns a 200.
    """
    host = User.objects.get(id=host_id)
    event = host.event_set.get(id=event_id)
    # print(host.id, event.id, event.unique_code)
    context = {}
    if unique_id != event.unique_code:
        context['return_status'] = 'Bad event url'
        return JsonResponse(context)
    
    if request.method == 'POST':

        ####################################################
        # # increment the number of clips received for this event
        clipnum = event.num_vid_clips = event.num_vid_clips+1
        event.save()
        ####################################################
        # Get the guest name (to use in the filename)
        guestsname = request.body.decode('utf-8')
        ####################################################
        # get a direct URL
        # https://stackoverflow.com/questions/21918046/google-cloud-storage-signed-urls-with-google-app-engine?lq=1
        rand4 = ''.join(random.choices(string.ascii_letters,k=4))
        fnamebase = str(clipnum)+'-'+rand4+'-'+guestsname
        video_title = fnamebase+'.video'
        cfile = os.path.join(
            str(host_id), str(event_id), 'orig', 
            video_title)
        abucket = storage.Client().bucket('gb-a')
        blob = storage.Blob(cfile, abucket)
        expiration_time = datetime.now()+timedelta(minutes=1)
        url = blob.generate_signed_url(expiration_time, version='v4', method='POST')
        context['url'] = url
        ####################################################
        # write to the database
        pfile = os.path.join(
            str(host_id), str(event_id), 'processed', 
            str(clipnum)+'-'+rand4+'-'+guestsname+'.mp4')
        tfile = os.path.join(
            str(host_id), str(event_id), 'thumbnails', 
            str(clipnum)+'-'+rand4+'-'+guestsname+'.jpg')
        mfile = os.path.join(
            str(host_id), str(event_id), 'minis', 
            str(clipnum)+'-'+rand4+'-'+guestsname+'.mp4')
        v = event.video_set.create(
            video_title=video_title,
            guest_name=guestsname,
            processedfpname=pfile,
            thumbnailfpname=tfile,
            minifpname = mfile,
            upload_date=datetime.now().strftime('%Y-%m-%d'),
            upload_time=datetime.now().strftime('%H:%M'),
        )
        context['vid'] = v.id
        return JsonResponse(context)
    else:
        context['return_status'] = 'Download the app'
    return render(request, 'guests/welcome.html', context)


@csrf_exempt
def process_video_non_cloud_task(request, host_id, event_id, unique_id,video_id):
    """
    The full video receiving and processing process is outlined in 
    serverapp.guests.views.post_vid_uid

    This is the non-cloud-task for handling success_action_redirect 
    after Guest has uploaded a video to google cloud storage.  
    It is used for debugging of the video processing. 
    When this is called, the Guest will not receive a success 200 response
    until after the video is completely processed.
    """
    print('inside non-cloud-task process video')
    host = User.objects.get(id=host_id)
    event = host.event_set.get(id=event_id)
    video = event.video_set.get(id=video_id)
    context = {}
    if unique_id != event.unique_code:
        context['return_status'] = 'Bad event url'
        return JsonResponse(context)

    cfile = os.path.join(
        str(host_id), str(event_id), 'orig', 
        video.video_title)
    print(cfile)
    create_standard_thumb_mini_videos(
         cfile, 
         video.processedfpname,
         video.thumbnailfpname,
         video.minifpname,
    )
    context['return_status'] = 'successfully processed'
    return JsonResponse(context)


@csrf_exempt
def process_video_create_cloud_task(request, host_id, event_id, unique_id,video_id):
    """
    The full video receiving and processing process is outlined in 
    serverapp.guests.views.post_vid_uid

    This handles the success_action_redirect 
    after Guest has uploaded a video to google cloud storage.  

    It kicks off a cloud task to process the video and returns
    a success 200 to the Guest.
    return: The status of the request through a JsonResponse
    """
    print('in process_video_create_cloud_task')
    ###############
    # verify host/event/video
    host = User.objects.get(id=host_id)
    event = host.event_set.get(id=event_id)
    video = event.video_set.get(id=video_id)
    context = {}
    if unique_id != event.unique_code:
        context['return_status'] = 'Bad event url'
        return JsonResponse(context)
    ###############
    # recreate the full path video title
    # TODO maybe this could be saved in the database???
    cfile = os.path.join(
        str(host_id), str(event_id), 'orig', 
        video.video_title)
    ############
    # create the cloud task
    ### # some of the stuff is pre-computed in GuestsConfig
    ### GUEST = apps.get_app_config('GuestsConfig')
    project = os.environ.get('MYPROJECT', 'thinking-glass-282301')
    queue = os.environ.get('MYQUEUE', 'vidprocessor0')
    location = os.environ.get('MYLOCATION', 'us-central1')
    
    client = tasks_v2.CloudTasksClient()
    # self.client = tasks_v2.CloudTasksClient.from_service_account_file('thinking-glass-282301-1175a1e8d2c6.json')
    parent = client.queue_path(project, location, queue)
    task = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': '/secret_url/processvideo/'
        }
    }
    body = {
        'infname': cfile,
        'processedfname': video.processedfpname,
        'thumbfname': video.thumbnailfpname,
        'mfname': video.minifpname,
    } 

    task['app_engine_http_request']['body'] = json.dumps(body).encode()
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(datetime.utcnow()) # pylint: disable=no-member
    task['schedule_time'] = timestamp
    print('just before client.create_task')
    response = client.create_task(
        parent=parent,
        task=task,
        # timeout = 1000,
    )
    print('in cct')
    return HttpResponse(response)


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


@csrf_exempt
def event_info(request, host_id, event_id, unique_id):
    """
    This will check to make sure the unique ID matches the host
    and event and then 
    :param request:
    :param host_id:
    :param event_id:
    :param unique_id:
    :return:
    """
    host = User.objects.get(id=host_id)
    event = host.event_set.get(id=event_id)
    data = {}
    if unique_id != event.unique_code:
        data['valid_flag'] = False
    else:
        data['valid_flag'] = True
        data['event_title'] = event.event_title
    return JsonResponse(data)



@csrf_exempt
def guest_welcome(request, host_id, event_id, unique_id):
    """
    This will check to make sure the unique ID matches the host
    and event and then 
    :param request:
    :param host_id:
    :param event_id:
    :param unique_id:
    :return:
    """
    context = {}
    return render(request, 'guests/welcome.html', context)



