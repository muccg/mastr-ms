import ldap
from django.contrib.auth.models import User, Group
from madas import settings
print 'finished imports'
class LDAPBackend():
    def authenticate(self, username=None, password=None):
        
        user = None

        # anonymous bind to server
        try:
            # using debug on local server ie not boromir
            print 'ldap: try'
            if settings.DEV_SERVER:
                'using DEV_SERVER'
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)            
            l = ldap.initialize(settings.AUTH_LDAP_SERVER)
            l.protocol_version = ldap.VERSION3
            l.simple_bind_s()

        except ldap.LDAPError, e:
            print "Ldap Error:\n%s" % e
            return None

        try:

            #
            # user test
            #
            userfilter = "(&(objectclass=person) (uid=%s))" % username
            result_id = l.search(settings.AUTH_LDAP_BASE, ldap.SCOPE_SUBTREE, userfilter, ['dn'])
            
            result_type, result_data = l.result(result_id, 0)

            # If the user does not exist in LDAP, Fail.
            if (len(result_data) != 1):
                print 'didnt exist'
                return None

            # Attempt to bind to the user's DN
            userdn = result_data[0][0]
            l.simple_bind_s(userdn,password)


            #
            # group membership test
            #
            groupfilter = '(&(objectClass=groupofuniquenames)(uniqueMember=%s)(cn=%s))' % (userdn, settings.AUTH_LDAP_GROUP)
            group_result_id = l.search(settings.AUTH_LDAP_GROUP_BASE, ldap.SCOPE_SUBTREE, groupfilter, ['cn'])
            group_result_type, group_result_data = l.result(group_result_id, 0)
            
            print 'id', group_result_id
            print 'type', group_result_type

            # If the group membership does not exist in LDAP, Fail.
            if (len(group_result_data) != 1):
                print 'member of no groups'
                return None

            #
            # The user existed and authenticated. Get the user
            # record or create one with no privileges.
            #
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:

                try:
                    group = Group.objects.get(name__exact=settings.DEFAULT_GROUP)
                except Group.DoesNotExist, e:
                    print "Group DoesNotExist: %s\n%s" % (settings.DEFAULT_GROUP, e)
                    return None
                
                user = User.objects.create_user(username,"")
                user.is_staff = True
                user.groups.add(group)
                user.save()

            # Success.
            print "Login Success %s" % user
            return user
           
        except ldap.INVALID_CREDENTIALS, e:
            # Name or password were bad. Fail.
            print "Ldap Exception:\n%s" % e
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
