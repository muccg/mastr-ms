#from django.utils import simplejson

#This class holds various attributes of a request,
#in order for them to be persisted over the course of a redirect etc. So it is good for landing pages after clicking on an external link but needing to authenticate inbetween, for example.
#it is intended to live on the session
#You get the URLState by calling getCurrentURLState and passing the request.
#You get data out of the urlstate with normal dot notation. If the 'key' doesn't exist, it will just return None rather than an exception.
#Internally, this class stores all the data in an internal _dict, which is easily clearable, and easy to export via json if we need it 

class URLState(object):
    def __init__(self, state=None):
        self.clear()
        if state is not None:
            self.__dict__['_dict'] = state
    def __getattr__(self, key):
        return self._dict.get(key, None)
    def __setattr__(self, key, value):
        self.__dict__['_dict'][key] = value
    def clear(self):
        self.__dict__['_dict'] = {}

    def get_state(self):
        return self._dict
        

def getCurrentURLState(request, andClear=False):
    #get existing urlstate, or create a new empty one.
    state = request.session.get('urlstate', None)
    urlstate = URLState(state)
    if andClear:
        request.session['urlstate'] = {}
    else:    
        #save it back, in case it is new
        request.session['urlstate'] = urlstate.get_state()
    return urlstate
