from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import userdata

def index(request):
    myusers = userdata.objects.all().values()
    template = loader.get_template('form.html')
    context = {
    'udatas': myusers,
    }
    return HttpResponse(template.render(context, request))

'''
def details(request,id):
    myuser = userdata.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
    'udata': myuser,
    }
    return HttpResponse(template.render(context, request))
'''
# Create your views here.