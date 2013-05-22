from mastrms.app.utils.data_utils import jsonResponse, jsonErrorResponse
from mastrms.users.MAUser import *
from mastrms.app.utils.mail_functions import sendRegistrationToAdminEmail
import logging
import mastrms.settings

logger = logging.getLogger('madas_log')

def submit(request, *args):
    '''This adds a new user into ldap with no groups
    '''
    detailsDict = getDetailsFromRequest(request)

    #check that the user doesn't already exist.
    if {} == loadMadasUser(detailsDict['username']):
        #if not, add the user
        adminUser = getMadasUser('nulluser') #a user who doesn't exist
        adminUser.IsAdmin = True #make them a priveleged user.
        #saveMadasUser will add the user if they do not exist already.
        success = saveMadasUser(adminUser, detailsDict['username'], detailsDict['details'], detailsDict['status'], detailsDict['password'])

        if not success:
            logger.warning("Could not add new user %s" % (detailsDict['username']))
        else:
            sendRegistrationToAdminEmail(request, settings.REGISTRATION_TO_EMAIL)

        return jsonResponse()
    else:
        logger.warning("User %s already existed, aborting registration" % (detailsDict['username']))
        raise Exception('User already exists')

