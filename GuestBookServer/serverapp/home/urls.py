# Copyright Mark B. Skouson, 2019

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verifylogout', views.verifylogout, name='verifylogout'),
    path('mylogin', views.mylogin, name='mylogin'),
]
