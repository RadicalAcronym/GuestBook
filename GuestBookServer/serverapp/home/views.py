from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    context = {}
    return render(request, 'home/index.html', context)

def verifylogout(request):
    context = {}
    return render(request, 'home/verifylogout.html', context)

def mylogin(request):
    context = {}
    return render(request, 'home/login.html', context)

