from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Widgets index")

def detail(request, widget_id):
    return HttpResponse("You're looking at widget %s." % widget_id)