from madas.utils import setRequestVars, jsonResponse, json_encode


def submit(request, *args):
    '''This adds a new user into ldap with no groups
    '''
    print '*** registration/submit ***' 

    import madas.users 
    from madas.users.views import _usersave, _userload
    
    if {} == _userload(request.REQUEST['email']):
        oldstatus, status =  _usersave(request, request.REQUEST['email'], admin=False)
        
        #HACK, save again to try to put the password in
        oldstatus, status =  _usersave(request, request.REQUEST['email'], admin=False)

        from mail_functions import sendRegistrationToAdminEmail
        
        sendRegistrationToAdminEmail(request, 'trac-nema@ccg.murdoch.edu.au')
        
        setRequestVars(request, success=True, data = None, totalRows = 0, authenticated = True, authorized = True, mainContentFunction='login')
    else:
        setRequestVars(request, success=False, data = None, totalRows = 0, authenticated = True, authorized = True, mainContentFunction='error:existingRegistration')

    print '*** registration/submit end ***' 
    return jsonResponse(request, [])