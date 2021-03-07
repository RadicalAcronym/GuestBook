from django.urls import path
from . import views
from .views import HostEventList

urlpatterns = [
    # path('', views.index, name='index'),
    path('host_home', views.host_home, name='host_home'),
    # path('host_home2/', HostEventList.as_view()),
    path(
        'get_qrcode/<int:event_id>/',
        views.get_qrcode_uid,
        name='get_qrcode_uid',
    ),
    path('create_event',
         views.create_event,
         name='create_event'),
    path('edit_event/<int:event_id>/',
         views.edit_event,
         name='edit_event'),    
    path(
        'view_videos/<int:event_id>/',
        views.view_videos,
        name='view_videos',
    ),
    path(
        'preview_clip/<int:video_id>/',
        views.preview_clip,
        name='preview_clip',
    ),
 
]
