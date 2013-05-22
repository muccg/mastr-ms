import datetime
import decimal
from django.contrib.auth.models import User
from mastrms.repository.models import Sample
from django.db import models
from types import *

def makeJsonFriendly(data):
    '''Will traverse a dict or list compound data struct and
    make any datetime.datetime fields json friendly
    '''

    try:
        if type(data) in [int, str, bool, NoneType]:
            return data
        #convert lists
        elif isinstance(data, list):
            for e in data:
                e = makeJsonFriendly(e)
        #convert keys
        elif isinstance(data, dict):
            for key in data.keys():
                data[key] = makeJsonFriendly(data[key])

        elif isinstance(data, datetime.time):
            return str(data.hour) + ':' + str(data.minute).rjust(2,'0')

        elif isinstance(data, User):
            return {'id':data.id, 'username':data.username}

        elif isinstance(data, Sample):
            return data.id
        else:
            #for everything else
            return str(data)

    except Exception, e:
        print 'makeJsonFriendly encountered an error: ', str(e)
    return data
