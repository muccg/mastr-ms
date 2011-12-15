#
#
# This tool is to import ldap user details across to become UserDetail entries.
#
# First the groups are imported
#
# One by one, user details are pulled over. If the user doesn't have a UserDetail object, 
# it is created. If they do, it is updated.
# 
# The user is then added to their groups.
#
from ccg.auth.ldap_helper import LDAPSearchResult, LDAPHandler
import settings
from users.models import Group, UserDetail
from django.contrib.auth.models import User

def import_ldap_groups():

    ld = LDAPHandler()
    grouplist = ld.ldap_list_groups()
    for group in grouplist:
        try:
            Group.objects.get(name=group)
            print 'Group %s already existed.' % (group)
        except:
            g = Group()
            g.name = group
            try:
                g.save()
                print 'Created group %s.' % (group)
            except Exception, e:
                print 'Could not create group %s: %s' % (group, e)

def set_user_details(user, ldap_details):
    try:
        (userdetails, created) = UserDetail.objects.get_or_create(user=user)
        if created:
            print 'creating user details for %s' % user.username
        else:
            print 'updating user details for %s' % user.username
        userdetails.set_from_dict(ldap_details)
        userdetails.save()

    except Exception, e:
        print 'Could not set user details for %s: %s' % (user.username, e)
def set_user_groups(user, ldap_groups):
    for group in ldap_groups:
        try:
            dbgroup = Group.objects.get(name=group)
            dbgroup.user.add(user)
            dbgroup.save() #checking debug
        except Exception, e:
            print 'Could not add %s to group %s: %s' % (user.username, group, e)

#def get_ldap_password(ldap_details):
#    password = None
#    ldappassword = ldap_details.get('userPassword', None)
#    if ldappassword is not None:
#        #ldap passwords are {scheme}hash, unsalted.
#        #the hash is base64 encoded
#        scheme
#     
#        b = base64.b64decode(the ldap hash)
#        e = ""
#        for c in b:
#            e += hex(ord(c))[2:]
#        #e is now the correst string for django


def create_or_update_user(username, ldap_details, ldap_groups):
    #create the user if they dont exist.
    (user, created) = User.objects.get_or_create(username=username)
    if created:    
        print 'Creating user %s' % (username)
    else:
        print 'Updating user %s' % (username)
  
    #we may not even need to import passwords??
    #or perhaps we only import passwords when db has no pw?

    #if ldap_details.has_key('userPassword'):
    #    #admin bid can access the 'userPassword' field.
    #    print 'pwd: ldap=%s, db=%s' % (ldap_details['userPassword'], user.password)
    #else:
    #    print 'no password for %s' % (user.password)
    
    set_user_groups(user, ldap_groups)
    set_user_details(user, ldap_details)

def import_ldap_users():

    ld = LDAPHandler(settings.LDAPADMINUSERNAME, settings.LDAPADMINPASSWORD)
    groupslist = ld.ldap_list_groups()
    userlist = ld.ldap_list_users(groupslist, method='or')
    print 'Found %d users.' % (len(userlist))
    for user in userlist:
        username = user['uid'][0]
        usergroups = ld.ldap_get_user_groups(username)
        userdetails = ld.ldap_get_user_details(username)
        create_or_update_user(username, userdetails, usergroups)


def import_ldap_data():
    import_ldap_groups()
    import_ldap_users()


