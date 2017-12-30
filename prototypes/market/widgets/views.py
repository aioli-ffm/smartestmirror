from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.list import ListView
from . import walker
from .httpresponsepaymentrequired import HttpResponsePaymentRequired
import os
from . import payment

def index(request):
    widgets_list = walker.all("widgets/widgets")
    context = {'object_list': widgets_list}
    return render(request, 'widgets_list.html', context)

def detail(request, widget_id):
    widget = walker.widget("widgets/widgets/"+widget_id+".json")
    context = {'widget': widget}
    return render(request, 'widget_detail.html', context)

def download(request, widget_id):
    try:
        widget = walker.widget("widgets/widgets/"+widget_id+".json")
        payment_ = payment.Payment('ESJYJSXVXZZJGWCHDEZQHWWMZNHGJIBXPEENUGOBTNKKFINXSSB9PAWIUITRUCB9VMLLKCASHO99OYYJDMWTVJXSLZ')
        if payment_.payed(widget_id, widget['value']):
            with open("widgets/widgets/"+widget_id+".py", 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/x-python")
                response['Content-Disposition'] = 'inline; filename=' + widget_id+'.py'
                return response
    except FileNotFoundError:
        return HttpResponseNotFound("Widget not found")
    return HttpResponsePaymentRequired(widget_id) 
