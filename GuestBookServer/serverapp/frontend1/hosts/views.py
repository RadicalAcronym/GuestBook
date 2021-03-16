# Copyright 2020 Mark B. Skouson
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import User, Event, Video
from .forms import EventForm
from datetime import datetime, timedelta

import os
import string
import random
import segno
from datetime import date
from google.cloud import storage
import io
import json

# Create your views here.


@login_required
def host_home(request):
    '''
    show the host the past and upcoming events they have scheduled
    '''
    user = request.user
    past_events = user.event_set.filter(event_date__lt=date.today())
    sched_events = user.event_set.exclude(event_date__lt=date.today())
    event_num_dict = {}
    for event in user.event_set.all():
        l = len( event.video_set.all() )
        event_num_dict[event.id] = l 
    context = {'past_events': past_events, 'sched_events': sched_events, 'event_num_dict': event_num_dict}
    return render(request, 'hosts/hosteventlist.html', context)

# This following class was a try at an alternate way to do host_home above.  In the end, it didn't
# Seem any easier, so I quit.
# TODO remove this
class HostEventList(LoginRequiredMixin, ListView):
    template_name = 'hosts/host_event_list.html'
    model = Event
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add contexts
        context['past_events'] = self.model.objects.filter(
            user=self.request.user).filter(
            event_date__lt=date.today())
        context['sched_events'] = self.model.objects.exclude(event_date__lt=date.today())
        return context

@login_required
def get_qrcode_uid(request, event_id):
    """
    This will check to make sure the unique ID matches the host
    and event and then create the qr code
    :param request:
    :param host_id:
    :param event_id:
    :param unique_id:
    :return:
    """
    user = request.user
    check = user.event_set.filter(pk=event_id)
    if len(check) != 1:
        return HttpResponseRedirect('/hosts/host_home')
    event = check[0]

    # Put it in a cloud bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket('gb-a')
    oname = os.path.join(str(user.id), str(event.id), 'qr', 'qrcode.png')
    # oname has no leading /
    blob = bucket.blob(oname)
    qr_text = 'https://thinking-glass-282301.uc.r.appspot.com/guests/'+\
        str(user.id)+'/'+str(event.id)+'/'+str(event.unique_code)
    img_buffer = io.BytesIO()
    segno.make(qr_text).save(img_buffer, kind='png', scale=5)
    img_buffer.seek(0)
    blob.upload_from_file(img_buffer)
    ####################################################
    # get a direct URL
    # abucket = storage.Client().bucket('gb-a')
    # blob = storage.Blob(oname, abucket)
    expiration_time = datetime.now()+timedelta(minutes=1)
    url = blob.generate_signed_url(expiration_time, version='v4', method='GET')
    # print('url', url)
    context = {'host': user, 'event': event, 'qr_text': qr_text, 'url': url}
    return render(request, 'hosts/show_qrcode.html', context)
    # return render(request, 'hosts/uploadsuccess.html', context)

@login_required
def create_event(request):
    # this method can be accessed either as a get (first time) or post (return when the form is filled out)
    if request.method == 'POST':
        form = EventForm(request.POST)
        # print(form.data)
        if form.is_valid():
            host = request.user
            rand10 = ''.join(random.choices(string.ascii_letters,k=10))
            # print('cleaned_data= ', form.cleaned_data)
            e = host.event_set.create(
                event_title=form.cleaned_data['event_title'],
                event_date=form.cleaned_data['event_date'],
                event_time=form.cleaned_data['event_time'],
                num_vid_clips=0,
                max_num_vid_clips=100,
                unique_code = rand10
            )
            return HttpResponseRedirect('/hosts/host_home')
    else:
        # print('get')
        form = EventForm()
    context = {'form': form}
    return render(request, 'hosts/create_event.html', context)

@login_required
def edit_event(request, event_id):
    user = request.user
    instance = Event.objects.all().filter(pk=event_id)
    if len(instance) != 1:
        print("Did not find the event you were looking for (#111)")
        return HttpResponseRedirect('/hosts/host_home')
    instance = instance[0]
    if instance.user != user:
        print("Did not find the event you were looking for (#112)")
        return HttpResponseRedirect('/hosts/host_home')
    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)
        print(form.data)
        if form.is_valid():
        #     print('cleaned_data= ', form.cleaned_data)
        #     instance.event_title=form.cleaned_data['event_title']
        #     instance['event_date']=form.cleaned_data['event_date']
        #     instance['event_time']=form.cleaned_data['event_time']
            form.save()
            return HttpResponseRedirect('/hosts/host_home')
    else:
        print('get')
        form = EventForm(instance=instance)
    context = {'form': form, 'event_id': event_id}
    return render(request, 'hosts/edit_event.html', context)


@login_required
def view_videos(request, event_id):
    user = request.user
    # Check that user owns the event
    check = user.event_set.filter(pk=event_id)
    # if doesn't own send back to host_home
    if len(check) != 1:
        return HttpResponseRedirect('/hosts/host_home')
    event = check[0]

    ####################################################
    # get a direct URL for each thumbnail
    # storage_client = storage.Client.from_service_account_json(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
    storage_client = storage.Client()
    storage_client = storage.Client.from_service_account_json(
        os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    )
    bucket = storage_client.bucket('gb-a')
    # make sure a unique sequential position number 
    vset = event.video_set.all()
    for i,r in enumerate(vset):
        r.position = i
    event.video_set.bulk_update(vset,['position'])
    thumblist = []
    for v in event.video_set.all():
        blob = bucket.blob(v.thumbnailfpname)
        # Good for 1 minute
        expiration_time = datetime.now()+timedelta(minutes=20)
        url = blob.generate_signed_url(expiration_time, version='v4', method='GET')
        thumblist.append((v.guest_name,v.id, url,))

    context = dict(
        host=user,
        event=event,
        event_id=event_id,
        thumburllist = thumblist
    ) 
    return render(request, 'hosts/eventvideolist.html', context)

@login_required
def preview_clip(request, video_id):
    user = request.user
    video = Video.objects.all().filter(pk=video_id)
    if len(video) != 1:
        print("Did not find the video you were looking for (#113)")
        return HttpResponseRedirect('/hosts/host_home')
    video = video[0]
    event = video.event
    if event.user != user:
        print("Did not find the video you were looking for (#114)")
        return HttpResponseRedirect('/hosts/host_home')
    ####################################################
    # get a direct URL for the preview vid
    storage_client = storage.Client()
    bucket = storage_client.bucket('gb-a')
    blob = bucket.blob(video.minifpname)
    # Good for 1 minute
    expiration_time = datetime.now()+timedelta(minutes=1)
    url = blob.generate_signed_url(expiration_time, version='v4', method='GET')
    context = dict(
        host=user,
        event=event,
        video=video,
        url=url,
    )
    return render(request, 'hosts/preview_clip.html', context)

@login_required
def reorder_events(request):
    # print("inside reorder_events")
    received_payload = json.loads(request.body)
    # print(received_payload)
    startrow = received_payload['startrow']-1
    endrow = received_payload['endrow']-1
    user = request.user
    # Check that user owns the event
    check = user.event_set.filter(pk=received_payload['event_id'])
    # if doesn't own send back to host_home
    if len(check) != 1:
        return HttpResponseRedirect('/hosts/host_home')
    event = check[0]
    # TODO may be able to speed this up by seeing whether it is less to subtract rather than always adding
    if endrow > startrow:
        vset = event.video_set.all()[startrow:endrow+1]
        l = vset.count()
        # for i in range(l):
        #     print('1a',vset[i],vset[i].position)
        for i,r in enumerate(vset):
            if i==0:
                tmp = r.position
                r.position = vset[l-1].position
            else:
                r.position = tmp
                tmp +=1
        event.video_set.bulk_update(vset,['position'])
        # vset = event.video_set.all()[startrow:endrow+1]
        # for i in range(l):
        #     print('1b',vset[i],vset[i].position)
    if endrow < startrow:
        vset = event.video_set.all()[endrow:startrow+1]
        l = vset.count()
        # for i in range(l):
        #     print('2a',vset[i],vset[i].position)
        savepos = vset[0].position
        tmp = savepos
        for i,r in enumerate(vset):
            if i==l-1:
                r.position = savepos
            else:
                tmp +=1
                r.position = tmp
        event.video_set.bulk_update(vset,['position'])
        # vset = event.video_set.all()[endrow:startrow+1]
        # for i in range(l):
        #     print('2b',vset[i],vset[i].position)
    print('written', )
    return HttpResponse("Success")


