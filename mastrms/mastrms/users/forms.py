import logging
from .models import MADAS_USER_GROUP

logger = logging.getLogger("mastrms.users")

# fixme: this function duplicates django forms -- need to make a
# normal form which does the same thing.


def getDetailsFromRequest(request):
    '''This is a generic function for parsing the form data passed in
       via one of the user edit forms
       it returns a dictionary with the following format:
       email: <email supplied in form>
       password: <password supplied in form>
       details: <dict of other details as supplied in form>
       status: <dict of status information (node, admin, noderep etc)
    '''
    def getReqVarSTR(key, default=''):
        return str(request.REQUEST.get(key, default)).strip()

    # updateDict keys correspond to User model fields
    updatedemail = getReqVarSTR('email')
    updateDict = {}
    updateDict['email'] = updatedemail
    updateDict['telephoneNumber'] = getReqVarSTR('telephoneNumber')
    updateDict['physicalDeliveryOfficeName'] = getReqVarSTR('physicalDeliveryOfficeName')
    updateDict['title'] = getReqVarSTR('title')
    updateDict['first_name'] = getReqVarSTR('firstname')
    updateDict['last_name'] = getReqVarSTR('lastname')
    updateDict['homePhone'] = getReqVarSTR('homephone')  # fixme: homePhone -> homephone
    updateDict['postalAddress'] = getReqVarSTR('address')  # fixme: postalAddress -> address
    # fixme: description -> areaOfInterest
    updateDict['description'] = getReqVarSTR('areaOfInterest')
    # fixme: destinationIndicator -> dept
    updateDict['destinationIndicator'] = getReqVarSTR('dept')
    # fixme: businessCategory -> institute
    updateDict['businessCategory'] = getReqVarSTR('institute')
    # fixme: registeredAddress -> supervisor
    updateDict['registeredAddress'] = getReqVarSTR('supervisor')
    updateDict['carLicense'] = getReqVarSTR('country')  # fixme: carLicense -> country

    # any that are blank, we delete
    for key in updateDict.keys():
        if not updateDict[key]:
            del updateDict[key]

    statusDict = {}
    statusDict['admin'] = request.REQUEST.get('isAdmin')
    statusDict['noderep'] = request.REQUEST.get('isNodeRep')
    statusDict['mastradmin'] = request.REQUEST.get('isMastrAdmin')
    statusDict['projectleader'] = request.REQUEST.get('isProjectLeader')
    statusDict['mastrstaff'] = request.REQUEST.get('isMastrStaff')
    statusDict['node'] = request.REQUEST.get('node')
    status = request.REQUEST.get('status')
    if status == 'Active':
        status = MADAS_USER_GROUP
    statusDict['status'] = status
    password = getReqVarSTR('password').strip()  # empty password is ignored anyway

    retdict = {}
    retdict['email'] = updatedemail
    retdict['password'] = password
    retdict['details'] = updateDict
    retdict['status'] = statusDict

    logger.debug('Parsed Form results:')
    logger.debug('Email: %s', updatedemail)
    logger.debug('Password: %s', "*" * len(password))
    logger.debug('Details:')
    for key in updateDict.keys():
        logger.debug('%s : %s' % (key, updateDict[key]))
    logger.debug('Status:')
    for key in statusDict.keys():
        logger.debug('%s : %s' % (key, statusDict[key]))

    return retdict
