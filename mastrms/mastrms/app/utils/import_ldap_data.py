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
import re
import base64

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

    if len(ldap_groups)>1 and 'User' in ldap_groups:
        #if they are part of more than just the user group, then they aren't a client.
        #make them staff.
        user.is_staff = True
        user.save()

def bin_to_bytes(binstr):
    result = ""
    for c in binstr:
        result+="%0.2x" % (ord(c))
    return result

def django_password_from_ldap_password(ldap_details):
    rawdigest = None
    bindigest = None
    scheme = None
    salt = None
    digest = None
    djangopwstring = None
    ldappassword = ldap_details.get('userPassword', None)
    pwd_pattern = re.compile('{(\w+)}(.+)')
    if ldappassword is not None:
        ldappassword = ldappassword[0]
        #ldap passwords are {scheme}hash
        #the hash is base64 encoded
        pwd = pwd_pattern.match(ldappassword)
        if len(pwd.groups()) == 2:
            scheme = pwd.group(1)
            b64pwdhash = pwd.group(2)

            print 'scheme: %s' % (scheme)

            #convert the password hash to ascii
            #ldap password hashes are base64
            rawdigest = base64.b64decode(b64pwdhash)
            bindigest = bin_to_bytes(rawdigest)
            digest = ""
            #now for the scheme
            if scheme == 'MD5':
                digest = bin_to_bytes(rawdigest)
                djangopwstring = "md5$$" + digest
            elif scheme == 'SSHA':
                salt = rawdigest[20:]
                digest = bin_to_bytes(rawdigest[:20])
                djangopwstring = "sha1$%s$%s" % (salt, digest)

                #the above code is correct, except:
                # - OpenLDAP salts are randombytes, which can't be written to djangos db AND
                # - OpenLDAP passwords are pw+salt, but django passwords are salt+pw, so they won't match anyway.
                #So in short, we can't import these passwords
                djangopwstring = None

            else:
                print 'unknown password scheme: %s' % (scheme)

        else:
            print 'unknown password format'

    else:
        print 'no password to migrate'

    return (djangopwstring, rawdigest, bindigest, scheme, salt, digest)

def create_or_update_user(username, ldap_details, ldap_groups, failed_pw_list):
    #create the user if they dont exist.
    (user, created) = User.objects.get_or_create(username=username)
    if created:
        print 'Creating user %s' % (username)
    else:
        print 'Updating user %s' % (username)

    set_user_groups(user, ldap_groups)
    set_user_details(user, ldap_details)

    #we only import passwords when db has no pw
    if user.password in ['','!']:
        newpassword, rd, bd, sch, sa, di = django_password_from_ldap_password(ldap_details)
        if newpassword is not None:
            user.password = newpassword
            user.save()
        else:
            failed_pw_list.append(username)
    return failed_pw_list

def import_ldap_users():
    failed_pw_list = []
    ld = LDAPHandler(settings.LDAPADMINUSERNAME, settings.LDAPADMINPASSWORD)
    groupslist = ld.ldap_list_groups()
    userlist = ld.ldap_list_users(groupslist, method='or')
    print 'Found %d users.' % (len(userlist))
    for user in userlist:
        username = user['uid'][0]
        usergroups = ld.ldap_get_user_groups(username)
        userdetails = ld.ldap_get_user_details(username)
        create_or_update_user(username, userdetails, usergroups, failed_pw_list)
    return failed_pw_list

def import_ldap_data():
    import_ldap_groups()
    failed_pw = import_ldap_users()
    print 'The following user account passwords could not be imported:'
    for uname in failed_pw:
        print uname

def test_pw_migrate(username):
    ld = LDAPHandler(settings.LDAPADMINUSERNAME, settings.LDAPADMINPASSWORD)
    ldap_details = ld.ldap_get_user_details(username)
    newpassword, rd, bd, sch, sa, di = django_password_from_ldap_password(ldap_details)
    print 'Newpassworhashd: ', newpassword
    print 'Raw Digest: ', rd
    print 'Bin Digest: %s len=%d' %(bd, len(bd))
    print 'Scheme: ', sch
    print 'Salt: ', sa
    print 'Digest ', di

    return (newpassword, rd, sch, sa, di)

