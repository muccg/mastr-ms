from mastrms.app.utils.data_utils import jsonResponse, jsonErrorResponse
from mastrms.users.MAUser import *
from mastrms.app.utils.mail_functions import sendRegistrationToAdminEmail
import logging
from django.conf import settings

logger = logging.getLogger('madas_log')

def submit(request, *args):
    '''This adds a new user into ldap with no groups
    '''
    detailsDict = getDetailsFromRequest(request)

    username = detailsDict['username']
    user_exists = bool(loadMadasUser(username))

    if not user_exists:
        #if not, add the user
        adminUser = getMadasUser('nulluser') #a user who doesn't exist
        adminUser.IsAdmin = True #make them a priveleged user.
        #saveMadasUser will add the user if they do not exist already.
        user_exists = saveMadasUser(adminUser, username, detailsDict['details'], detailsDict['status'], detailsDict['password'])

        if not user_exists:
            logger.warning("Could not add new user %s" % (username))
    else:
        logger.warning("User %s already existed, skipping registration" % (username))

    if user_exists:
        sendRegistrationToAdminEmail(request, username,
                                     settings.REGISTRATION_TO_EMAIL)

    return jsonResponse()
