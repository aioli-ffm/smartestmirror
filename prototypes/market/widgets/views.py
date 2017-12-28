from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from . import walker
from .httpresponsepaymentrequired import HttpResponsePaymentRequired

def index(request):
    widgets_list = walker.all("widgets/widgets")
    context = {'object_list': widgets_list}
    return render(request, 'widgets_list.html', context)

def detail(request, widget_id):
    widget = walker.widget("widgets/widgets/"+widget_id+".json")
    context = {'widget': widget}
    return render(request, 'widget_detail.html', context)

def download(request, widget_id):
    return HttpResponsePaymentRequired(widget_id) 
