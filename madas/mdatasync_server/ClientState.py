import os
import os.path
import pickle
from django.conf import settings

LOGNAME = 'mdatasync_server_log'
logger = logging.getLogger(LOGNAME)

#This is an object which we will serialise to disk,
#representing a snapshot of client state. It is refreshed
#every time a client syncs
class ClientState(object):
    def __init__(self, org=None, site=None, station = None):
        self.files = {} #the list of files that the client reports it has
        self.lastSyncAttempt = None #the last time the client contacted the service
        self.organisation = org
        self.sitename = site
        self.station = station
        self.lastError = ""


def get_saved_client_state(org, site, station):
    #look for the file, if exists, try deserialising and returning
    clientstatedir = os.path.join(settings.REPO_FILES_ROOT , 'synclogs')
    clientstatefname = os.path.join(clientstatedir, "STATE_%s_%s_%s.dat" % (org, site, station))
    if os.path.exists(clientstatefname):
        try:
            with open(clientstatefname) as f:
                clientstate = pickle.load(f)
            return clientstate
        except Exception, e:
            logger.warning("%s could not be un-pickled: %s" % (clientstatefname, e) )
    else:
        logger.debug("File %s did not exist." % (clientstatefname) )
    #else reuturn a new Clientstate object
    return ClientState(org=org, site=site, station=station)

def save_client_state(clientstate):
    clientstatedir = os.path.join(settings.REPO_FILES_ROOT , 'synclogs')
    clientstatefname = os.path.join(clientstatedir, "STATE_%s_%s_%s.dat" % (clientstate.organisation, clientstate.sitename, clientstate.station))
    try:
        with open(clientstatefname, "wb") as f:
            pickle.dump(clientstate, f)
    except Exception, e:
        logger.warning("Could not save clientstate. %s" % (str(e)))

def get_node_from_request(request, organisation=None, sitename=None, station=None):
    retval = None
    
    if organisation is None:
        organisation = request.REQUEST('organisation', None)
    if sitename is None:
        sitename = request.REQUEST('sitename', None)
    if station is None:
        station = request.REQUEST('station', None)

    logger.debug("Searching for node org=%s, sitename=%s, station=%s" % (organisation, sitename, station))
    try:
        nodeclient = NodeClient.objects.get(organisation_name = organisation, site_name=sitename, station_name = station) 
        if nodeclient is None:
            logger.warning("No nodeclient existed with organisation=%s, sitename=%s, station=%s" % (organisation, sitename, station))
        else:
            retval = nodeclient
    except:
        pass

    return retval

