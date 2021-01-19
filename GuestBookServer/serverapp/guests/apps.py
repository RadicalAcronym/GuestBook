# Copyright Mark B. Skouson, 2020
from django.apps import AppConfig
import ffmpeg
import os
import pprint
from google.cloud import storage
from google.cloud import tasks_v2
import io
import json
import time
import copy


class GuestsConfig(AppConfig):
    name = 'guests'
    label = 'GuestsConfig'

    # def ready(self):
    #     project = os.environ.get('MYPROJECT', None)
    #     queue = os.environ.get('MYQUEUE', 'vidprocessor1')
    #     location = os.environ.get('MYOCATION', 'us-central1')
        
    #     self.client = tasks_v2.CloudTasksClient()
    #     self.client = tasks_v2.CloudTasksClient.from_service_account_file('thinking-glass-282301-1175a1e8d2c6.json')
    #     self.parent = self.client.queue_path(project, location, queue)
    #     self.task = {
    #         'app_engine_http_request': {
    #             'http_method': 'POST',
    #             'relative_uri': '/secret_url/processvideo/'
    #         }
    #     }
    #     print('***finished with setting up guests stuff')


class Configuration():
    WIDTH = 1280 # 16*80
    HEIGHT = 720 # 9:80 
    FPS = 30
    AUDIOBITRATE = 127000
    AUDIOSAMPLERATE = 44100
    CRF = 23 # https://trac.ffmpeg.org/wiki/Encode/H.264
             # zero=lossless, default=23, 51=worst
    # Encoding speed to compression ratio
    ENCSPEED_COMPRESS_RATIO = 'slow' # 'slow', 'slower', 'veryslow'
    THUMBSIZE= 160
    MINIHEIGHT = 160 # 10*16
    MINIFPS = 15
    MINICRF = 30
    MINIENCSPEED_COMPRESS_RATIO = 'slow'
    MINIAUDIOBITRATE = 64000
    MINIAUDIOSAMPLERATE = 22050

def create_standard_thumb_mini_videos(cfile, pfile, tfile, mfile):
    """
    Converts a video to 1280x720 (16:9) format
        #other options 1290x1080 (16:9)
    30 frames per second
    H.264 (mpeg-4)
    AAC stereo audio   

    inputs: 
        cfile: The full filepathname to the clip the guest uploaded 
            e.g. '/2/3/10-geil-me.mov'
        pfile: the partial name of the processed clip
            e.g. '2/3/10-geil-me.mp4'
            e.g. '2/3/10-geil-me.jpg'
    """
    # Get the specs for how to process the video 
    config=Configuration()
    # ctemp is the file uploaded by the guest
    #         e.g. '/2/3/10-geil-me.mov'
    # This next part creates a file called /tmp/ztemp with and with 
    # the same file extension as ctemp.
    # For gcloud, you have to use /tmp, because /tmp is a virtual drive.
    storage_client = storage.Client()
    abucket = storage_client.bucket('gb-a')
    _, file_extension = os.path.splitext(cfile)
    ctemp = "/tmp/ztemp"+file_extension
    print('****cfile',cfile)
    print('****ctemp',ctemp)
    # pull the original file off gcloud and write to file
    # ffmpeg requires it to read from a file (can't use filehandle)
    abucket.get_blob(blob_name=cfile).download_to_filename(ctemp)

    #############################
    # Reshape the video and audio
    create_standard_video(ctemp,'/tmp/zptemp.mp4',config)
    abucket.blob(pfile).upload_from_filename('/tmp/zptemp.mp4')

    #############################
    # Create the thumbnail
    create_thumbnail('/tmp/zptemp.mp4', '/tmp/zttemp.jpg', config)
    abucket.blob(tfile).upload_from_filename('/tmp/zttemp.jpg')
    os.system('rm /tmp/zttemp.jpg '+ctemp)

    ############################
    # Create the mini vid
    create_minivideo('/tmp/zptemp.mp4', '/tmp/zmtemp.mp4', config)
    abucket.blob(mfile).upload_from_filename('/tmp/zmtemp.mp4') 
    os.system('rm  /tmp/zmtemp.mp4 /tmp/zptemp.mp4')

def create_standard_video(infname,outfname,config):
    """ Converts a video file from infame to outfname 
        as specified by c the config file

        Inputs:
          infname (str): input video file name
          outfname (str): output video file name
          config (dict): configuration object
        Outputs:
          none
    """
    #############################
    # probe for the size
    print('AAAA Probing AAAA')
    probe = ffmpeg.probe(infname)
    print('ZZZZ Probing ZZZZ')
    win = probe['streams'][0]['width']
    hin = probe['streams'][0]['height']
    # compute what the scaled width will be
    wmid = (win/hin*config.HEIGHT)//2*2
    # print(win,hin,wmid)
    #############################
    # Graph for video process
    v1 = ffmpeg.input(infname)
    a1 = v1.audio
    v1 = ffmpeg.filter(v1.video, 'scale', -2, config.HEIGHT)
    v1 = ffmpeg.filter(v1, 'fps', fps=config.FPS)
    if wmid > config.WIDTH:
        v1 = ffmpeg.filter(v1, 'crop', config.WIDTH, config.HEIGHT, "(in_w-out_w)/2", "(in_h-out_h)/2")
    elif wmid < config.WIDTH:
        v1 = ffmpeg.filter(v1, 'pad', config.WIDTH, config.HEIGHT, "(out_w-in_w)/2", "(out_h-in_h)/2")
    v1 = ffmpeg.output(
        v1, a1,
        outfname,
        pix_fmt='yuv420p',
        vcodec='libx264',
        acodec='aac',
        audio_bitrate=config.AUDIOBITRATE,
        ar=config.AUDIOSAMPLERATE,
        ac=2,
        crf=config.CRF,
        preset=config.ENCSPEED_COMPRESS_RATIO, 
    )
    v1 = ffmpeg.overwrite_output(v1)
    print('AAAA starting resizing AAAA')
    ffmpeg.run(v1)
    print('ZZZZ ending resizing ZZZZ')
    
def create_thumbnail(infname,outfname,config):
    """ Creates a thumbnail picture from infame to outfname 
        as specified by c the config file

        Inputs:
          infname (str): input video file name
          outfname (str): output picture file name
          config (dict): configuration object
        Outputs:
          none
    """
    #############################
    # Graph for thumbnail process
    v1 = ffmpeg.input(infname)
    p1 = ffmpeg.filter(v1, 'scale', -2, config.THUMBSIZE)
    p1 = ffmpeg.filter(p1, 'crop', config.THUMBSIZE, config.THUMBSIZE, "(in_w-out_w)/2", 0)
    p1 = ffmpeg.output(
        p1, 
        outfname,
        vframes=1,
    )
    p1 = ffmpeg.overwrite_output(p1)
    print('AAAA thumbnail AAAA')
    ffmpeg.run(p1)
    print('ZZZZ thumbnail ZZZZ')
    
def create_minivideo(infname,outfname,config):
    """ Shrinks the processed video or quicker viewing

        Inputs:
          infname (str): input video file name
          outfname (str): output video file name
          config (dict): configuration object
        Outputs:
          none
    """
    #############################
    # Graph for video process
    v1 = ffmpeg.input(infname)
    a1 = v1.audio
    v1 = ffmpeg.filter(v1.video, 'scale', -2, config.MINIHEIGHT)
    v1 = ffmpeg.filter(v1, 'fps', fps=config.MINIFPS)
    v1 = ffmpeg.output(
        v1, a1,
        outfname,
        pix_fmt='yuv420p',
        vcodec='libx264',
        acodec='aac',
        audio_bitrate=config.MINIAUDIOBITRATE,
        ar=config.MINIAUDIOSAMPLERATE,
        ac=2,
        crf=config.MINICRF,
        preset=config.MINIENCSPEED_COMPRESS_RATIO, 
    )
    v1 = ffmpeg.overwrite_output(v1)
    ffmpeg.run(v1)
