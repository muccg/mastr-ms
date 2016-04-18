# Create your views here.
from d_madas.madas.views import AuthObject

from django.http import HttpResponse
from django.core import serializers
import json

def index(request, *args):
    a = AuthObject()
    a.mainContentFunction = 'dashboard'
    return HttpResponse(json.dumps(a.__dict__) )
