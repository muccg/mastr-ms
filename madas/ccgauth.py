import ldap
import django
from madas import settings
from django.contrib.auth.models import User, Group

#for LDAP search results helper
import ldif
from StringIO import StringIO
from ldap.cidict import cidict

CCGAUTH_DEBUG = False 

def debugprint(*args):
    if CCGAUTH_DEBUG:
        print args
    else:
        pass


class LDAPSearchResult:
    """A class to model LDAP results.
    """
    
    dn = ''

    def __init__(self, entry_tuple):
        """Create a new LDAPSearchResult object."""
        debugprint( 'Creating LDAPSearchResult item...')
        (dn, attrs) = entry_tuple
        if dn:
            self.dn = dn
        else:
            return

        self.attrs = cidict(attrs)

    def get_attributes(self):
        """Get a dictionary of all attributes.
        get_attributes()->{'name1':['value1','value2',...], 'name2: [value1...]}
        """
        return self.attrs

    def set_attributes(self, attr_dict):
        """Set the list of attributes for this record.

        The format of the dictionary should be string key, list of string 
        values. e.g. {'cn': ['M Butcher','Matt Butcher']}

        set_attributes(attr_dictionary)
        """
        self.attrs = cidict(attr_dict)

    def has_attribute(self, attr_name):
        """Returns true if there is an attribute by this name in the
        record.

        has_attribute(string attr_name)->boolean
        """
        return self.attrs.has_key( attr_name )

    def get_attr_values(self, key):
        """Get a list of attribute values.
        get_attr_values(string key)->['value1','value2']
        """
        return self.attrs[key]

    def get_attr_names(self):
        """Get a list of attribute names.
        get_attr_names()->['name1','name2',...]
        """
        return self.attrs.keys()

    def get_dn(self):
        """Get the DN string for the record.
        get_dn()->string dn
        """
        return self.dn

    def pretty_print(self):
        """Create a nice string representation of this object.

        pretty_print()->string
        """
        str = "DN: " + self.dn + "\n"
        for a, v_list in self.attrs.iteritems():
            str = str + "Name: " + a + "\n"
            for v in v_list:
                str = str + "  Value: " + v + "\n"
        str = str + "========"
        return str

    def to_ldif(self):
        """Get an LDIF representation of this record.

        to_ldif()->string
        """
        out = StringIO()
        ldif_out = ldif.LDIFWriter(out)
        ldif_out.unparse(self.dn, self.attrs)
        return out.getvalue()


class LDAPHandler():
    def __init__(self, userdn=None, password=None):
        '''This class makes use of the 'settings' module, which should be accessible from the current scope.'''
        try:
            #Check to see if this is a dev server.
            if settings.DEV_SERVER:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)            
            #initialise LDAP server connection
            self.l = ldap.initialize(settings.AUTH_LDAP_SERVER)
            self.l.protocol_version = ldap.VERSION3
            if (userdn is None):
                #bind using simple auth or Kerberos if available
                self.l.simple_bind_s()
                debugprint('Anonymous bind OK')
            else:
                self.l.simple_bind_s(userdn + ',' + settings.AUTH_LDAP_ADMIN_BASE, password)
        except ldap.LDAPError, e:
            debugprint("Ldap Error:\n%s" % e)
            return None

        #Otherwise, set a few variables for later use
        self.BASE = settings.AUTH_LDAP_BASE
        self.GROUP = settings.AUTH_LDAP_GROUP
        self.GROUP_BASE = settings.AUTH_LDAP_GROUP_BASE
        self.USER_BASE = settings.AUTH_LDAP_USER_BASE
        self.SERVER = settings.AUTH_LDAP_SERVER
        self.GROUPOC = 'groupofuniquenames'
        self.USEROC = 'inetorgperson'
        self.MEMBERATTR = 'uniqueMember'
        self.USERDN = 'ou=People'
  
    def get_search_results(self, results):
        """Given a set of results, return a list of LDAPSearchResult objects.
        """
        res = []

        if type(results) == tuple and len(results) == 2 :
                (code, arr) = results
        elif type(results) == list:
                arr = results

        if len(results) == 0:
                return res

        for item in arr:
                res.append( LDAPSearchResult(item) )

        return res


    def ldap_query(self, base=None, scope=ldap.SCOPE_SUBTREE, filter="", rattrs=None, timeout=0):
        '''base is the ldap base to search on
           scope is the scope of the search (depth of descendant searches etc)
           userfilter is the user supplied filter information ( a string)
           rattrs is the format of the result set
        '''
        if base is None:
            base = self.BASE #this is done here because we cant access self in the function header

        retval = []
        try:
            debugprint('LDAP Query: ', base, scope, filter, rattrs)
            #result_id = self.l.search(base, scope, filter, rattrs)            
            #result_type, result_data = self.l.result(result_id, timeout)
            result_data = self.l.search_s(base, scope, filter, rattrs)
            retval = self.get_search_results(result_data)
            #for val in retval:
            #    print val.pretty_print()
        except Exception, e:#ldap.LDAPError, error_message:
            debugprint('LDAP Query Error: ', str(e))
            #print 'LDAP Query Error: ', error_message           
        return retval
    
    def ldap_list_groups(self):
        '''returns a list of group names'''
        debugprint('***ldap_list_groups: ***' )   
        
        groupdn = self.GROUP_BASE 
        userfilter = '(objectClass=%s)' % (self.GROUPOC)
        result_data = self.ldap_query(base=groupdn, filter=userfilter)
        groups = []
        for result in result_data:
            #print result.pretty_print()
            for g in result.get_attr_values('cn'):
                groups.append(g)
        return groups
        
 
    def ldap_get_user_details(self, username):
        ''' Returns a dictionary of user details.
            Returns empty dict on fail'''
        #Get application user details (only users in the application's LDAP tree) 
        debugprint('***ldap_get_user_details***')
        #TODO: Replace this searchbase with an app variable
        searchbase = 'ou=NEMA, ou=People, dc=ccg, dc=murdoch, dc=edu, dc=au'
        result_data = self.ldap_query(base=searchbase, filter = "uid=%s" % (username) )            
        if len(result_data) > 0:
            #TODO: merge in group data
            userdetails = result_data[0].get_attributes()
            try:
                a = self.ldap_get_user_groups(username)
                debugprint('\tThe User Groups were:', a)

                userdetails['groups'] = a 
            except Exception, e:
                debugprint( '\tException: ', str(e) )
            #print 'Printing the first result of get_user_details:', userdetails 
                
            return userdetails

        else:
            debugprint('\tldap_get_user_details returned no results: uid=', username)
            #user doesn't exist
            #this can happen when a dummy user has been inserted into a group.
            return {}


    def ldap_update_user(self, username, newusername, newpassword, detailsDict, pwencoding=None):
        '''You will need an authenticated connection with admin privelages to update user details in LDAP'''
        debugprint('***ldap_update_user****')
        #if the new username is different to the old username, 
        #cache the current groups for this user.
        if newusername is None:
            newusername = username
        
        if username != newusername: 
            cachedGroups = self.ldap_get_user_groups(username)
            debugprint('\tUsername was different. Cached groups are: ', cachedGroups)

        #search for the user DN to make sure we aren't renaming to an existing name.
        debugprint('checking to see if new DN exists')
        newdn = self.ldap_get_user_dn(newusername)
        if newdn is not None:
            if newusername != username:
                #no good. Trying to rename to an existing username
                debugprint( '\tNew Username already existed.')
                return
       
        debugprint('\tpreparing data') 
        #prepare data
        detailsDict['objectClass'] = ['top', 'inetOrgPerson', 'simpleSecurityObject', 'organizationalPerson', 'person']
        detailsDict['uid'] = newusername #setting the new username
      
        if newpassword is not None and newpassword != '':
            debugprint( 'encoding new password') 
            #time to encode the password:
            encpassword = ''
            #newpassword = newpassword.strip()
            debugprint( 'PW:', newpassword )
            if pwencoding is None:
                #No encoding
                encpassword = newpassword
            elif pwencoding == 'md5':
                #MD5 encoding
                import md5 
                import base64 
                m = md5.new()
                m.update(newpassword)
                debugprint( 'doing md5')
                encpassword = '{MD5}%s' % (base64.encodestring( m.digest()) ) 
            #Insert other encoding schemes here.            

            detailsDict['userPassword'] = encpassword.strip()
            debugprint( 'finished encoding' )
        debugprint( 'looking up old user')
        #ok now look up the user to update. Make sure we look them up using the old name.
        dn = 'uid=%s, %s' % (username, self.USER_BASE) #BASE not quite right
                                                             #needs to be 'ou=NEMA','ou=People', 'dc=ccg,dc=murdoch,dc=edu,dc=au',
        newparent = self.USER_BASE #we are going to need AUTH_LDAP_USER_BASE- as above.
        newrdn = 'uid=%s' % (username)
        
        #rename the user if required
        if username != newusername:
            debugprint( 'renaming user')
            try:
                r = self.l.rename_s(dn, newrdn, newsuperior=newparent, delold=true)
                #Change the dn, so we use this one from now on in the update
                dn = "%s, %s" % (newrdn, newparent) 
            except Exception, e:
                debugprint ('User rename failed. ' + str(e))
        
        debugprint('Editing User: ' + dn)
        try:
            userfilter = "(&(objectclass=person) (uid=%s))" % username
            usrs = self.ldap_query(filter = userfilter, base=self.USER_BASE)
            if len(usrs) != 1:
                raise Exception, "More than one user found for %s" % (username)
            old = usrs[0]
            debugprint ('OLD: ')
            o = old.get_attributes()
            for k in o.keys():
                debugprint("Key %s, value: %s" % (k, o[k]))
            
            for k in detailsDict.keys():
                v = detailsDict[k]
                if not isinstance(v, list):
                    detailsDict[k] = [v] 
            debugprint('NEW: ')
            for k in detailsDict.keys():
                debugprint("Key %s, value: %s" % (k, detailsDict[k]) )

            #Test equality of sets.
            for k in detailsDict.keys():
                if not o.has_key(k):
                    debugprint ('Key %s not present in OLD' % (k) )
                elif o[k] != detailsDict[k]:
                    debugprint( 'Value for %s different. %s vs %s' % (k, o[k], detailsDict[k]) )
                else:
                    debugprint('new and old values for %s are the same' % (k) )
            debugprint('finished testing')
            import ldap.modlist as modlist
            mods = modlist.modifyModlist(old.get_attributes(), detailsDict, ignore_oldexistent=1)
            
            debugprint('Mods: ')
            for t in mods:
                print t
            if len(mods) > 0:
                r = self.l.modify_ext_s(dn, mods)
        except Exception, e:
            debugprint('Error editing user: ', str(e) )
            
        return

    def ldap_add_user(self, username, detailsDict, pwencoding=None, objectclasses=[]):
        '''You need to have used an admin enabled username and password to successfully do this'''
        username = username.strip()
        f = "(&(objectclass=person) (uid=%s))" % username
        usrs = self.ldap_query(filter = userfilter, base=self.USER_BASE)
        retval = False
        if len(usrs) != 0:
            #user already existed!
            debugprint('\tA user called %s already existed. Refusing to add.')
        else:
            try:
                debugprint('\tPreparing to add user %s')
                dn = 'uid=%s,%s,%s,%s' % (username, usercontainer, userdn, basedn)
                from copy import deepcopy
                data = deepcopy(detailsDict)
                data['objectclass'] = objectclasses

                newattrs = []
                for key in data:
                    newattrs.append( (str(key), str(data[key])) )

                #so now newattrs contains a list of tuples, which are key value pairs.
                debugprint('Calling ldap_add: %s and %s' % (dn, str(newattrs)) )
                res = self.l.add_s(dn, newattrs)
                #TODO interrogate res
                retval = True
            except Exception, e:
                print 'Exception adding LDAP user: ', str(e)
        return retval

    def ldap_add_group(self, groupname):
        '''You need to have used an admin enabled username and password to successfully do this'''
        debugprint('***ldap_add_group***')
        groupname = groupname.strip()
        f = '(objectClass=groupOfUniqueNames)'
        groupresult = self.ldap_query(base = self.GROUP_BASE , filter = f, rattrs = ['cn'])
        for groupres in groupresult:
            if groupname == groupres.get_attr_values('cn')[0]:
                return False
       
        #ok so we are good to go.
        debugprint('preparing to add group')
        newattrs = []
        newattrs.append( ('cn', groupname) )
        newattrs.append( ('objectClass', self.GROUPOC) )
        newattrs.append( ('uniqueMember', 'uid=dummy') )

        dn = 'cn=%s,%s' % (groupname, self.GROUP_BASE)
        debugprint('calling ldap_add:', dn, ' AND ', newattrs)
        try:
            res = self.l.add_s(dn, newattrs)
        except Exception, e:
            debugprint('ldap_add_group: Exception in ldap_add: ', str(e) )
            return False
        debugprint('the response from the add command was: ', res)

        return True

    def ldap_rename_group(self, oldname, newname):
        '''You need to have used an admin enabled username and password to successfully do this'''
        debugprint('***ldap_rename_group***')
        
        dn = 'cn=%s,%s' % (oldname.strip(), self.GROUP_BASE)
        newrdn = 'cn=%s' % (newname.strip())
        try:
            ret = self.l.rename_s(dn, newrdn) #by default removes the old one (delold=1)
            
        except Exception, e:
            debugprint('Couldn\'t rename group %s: %s' % (oldname, str(e)) )
            return False
        
        return True


    def ldap_delete_group(self, groupname):
        '''You need to have used an admin enabled username and password to successfully do this'''
        '''CAUTION: This function will delete any group passed to it.
           You need to have sanity checked the group you are trying to delete BEFORE
           calling this function.'''
        debugprint('ldap_delete_group')
        dn = 'cn=%s,%s' % (groupname.strip(), self.GROUP_BASE)
        try:
            ret = self.l.delete_s(dn)
        except Exception, e:
            debugprint('Couldn\'t delete group %s: %s' % (groupname, str(e))  ) 
            return False

        return True

    def ldap_get_user_groups(self, username):
        
        debugprint('***ldap_get_user_groups:enter***')
        udn = self.ldap_get_user_dn(username)
        if udn is None:
            return None
        
        f = '(&(objectClass=%s)(%s=%s))' % (self.GROUPOC, self.MEMBERATTR, udn)    
        #f = '(&(objectclass=groupofuniquenames)(uniquemember=uid=bpower@ccg.murdoch.edu.au,ou=NEMA,ou=People,dc=ccg,dc=murdoch,dc=edu,dc=au))'
        result_data = self.ldap_query(base=self.GROUP_BASE,filter=f)            
        #result_data = self.ldap_query(base='dc=ccg,dc=murdoch,dc=edu,dc=au', filter=f)            
        groups = []
        for result in result_data:
            #print '***', result.pretty_print()
            for g in result.get_attr_values('cn'):
                groups.append(g) 
        
        if len(groups) == 0:
            debugprint('ldap_get_user_groups returned no results.')
        debugprint('***ldap_get_user_groups:exit***')
      
        return groups  
            
    def ldap_get_user_dn(self, username):
        result_data = self.ldap_query(filter='uid=%s' % (username))
        if len(result_data) > 0:
            dn = result_data[0].get_dn()
            debugprint('User DN found as: ', dn)
            return dn
        else:
            debugprint('Username not found!')       
            return None            

    def ldap_list_users(self, searchGroup, method = 'and'):
        '''expects searchGroup to be a list of groups to search
           fetches an array of user detail dictionaries
           default method is 'and' (need to be in all groups specified)
           other acceptible method is 'or' (can be in any of the groups)
           '''
        debugprint ('***ldap_list_users: enter ***')
        
        
        #searchGroup.append('*') 
        
        userlists = []
        for groupname in searchGroup:
            g = []
            #TODO: search for all users in the group
            filter = 'cn=%s' % (groupname)
            userlist = self.ldap_search_users(filter = filter, base=self.GROUP_BASE)
            debugprint('USERLIST: ', userlist)
            for user in userlist:
                g.append(user)
            userlists.append(g)

        #so now, users is a list of lists.
        #the first thing to do is get a list of distinct usernames.
        distinct_users = []
        for g in userlists:
            for user in g:
                if user not in distinct_users:
                    distinct_users.append(user)

        #if the method is 'and', then we are returning a list of users that are in all the groups.
        retusers = []
        if method == 'and':
            for user in distinct_users:
                in_all = True
                for g in userlists:
                    if user not in g:   
                        in_all = False
                if in_all:
                    retusers.append(user)

        else:
            retusers = distinct_users #users in any group


        debugprint('***ldap_list_users: exit***')
        return retusers

    def ldap_search_users(self, base, filter):
        '''returns a list of users, each user being a dict'''
        debugprint('***ldap_search_users : enter***')
        results = self.ldap_query(filter=filter, base=base)
       
        users = []
        for result in results:
            #print 'RESULTS', result.pretty_print()
            if result.has_attribute('uniquemember'):
                userresults = result.get_attr_values('uniquemember')
                #print 'USERRESULTS: ', userresults
                for user in userresults:
                    debugprint( '\tUSER: ', user )
                    #retrieve the details of this useer.
                    prefix, uname =user.split('=', 1)
                    uname = uname.split(',', 1)[0]
                    #print uname
                    userdetails = self.ldap_get_user_details(uname)
                    #print userdetails.pretty_print()
                    if len(userdetails) > 0:
                        users.append(userdetails)
        debugprint('***ldap_search_users : exit***')
        return users

    def ldap_add_user_to_group(self, username, groupname):
        '''adds a user to a group
           returns true on success
           returns false on fail (user didnt exist, group didn't exist)'''
        debugprint('***ldap_add_user_to_group*** : enter') 
        retval = False
        ud = self.ldap_get_user_details(username)
        if len(ud) > 0: #does the user exist?
            #already have this group?
            if groupname in ud['groups']:
                debugprint('\tUser already in group')
                retval = True #they were already in the group
            else:
                #does the new group exist?
                if groupname in self.ldap_list_groups():
                    debugprint('\tCandidate group existed')
                    #add the user to the group
                    #get group dn:
                    gresult = self.ldap_query(base=self.GROUP_BASE, filter='(&(objectclass=groupofuniquenames) (cn=%s))' % groupname)
                    if len(gresult) != 0:
                        try:
                            gdn = gresult[0].get_dn()
                            udn = self.ldap_get_user_dn(username)
                            #modify the group's attrubutes so as to add this entry
                            import ldap.modlist as modlist
                            old = gresult[0]
                            oldattrs = old.get_attributes()
                            import copy
                            newattrs = copy.deepcopy(oldattrs)
                            debugprint('oldattrs: ', old.get_attributes())
                            #catch code for empty groups (no 'uniquemmembers')
                            if not newattrs.has_key('uniqueMember'):
                                newattrs['uniqueMember'] = []
                            newattrs['uniqueMember'].append(udn) 
                            mods = modlist.modifyModlist(oldattrs, newattrs, ignore_oldexistent=1)
                            debugprint('MODS:%s' % (str(mods)))
                            if len(mods) > 0:
                                r = self.l.modify_ext_s(gdn, mods)
                            retval = True
                        except Exception, e:
                            print 'Exception adding user %s to group %s: %s' % (username, groupname, str(e)) 

                    else:
                        debugprint('\tCouldn\'t get group dn')
                else:
                    debugprint('\tCandidate group didn\'t exist. Aborting')

        debugprint('***ldap_add_user_to_group*** : exit') 
        return retval


    def ldap_remove_user_from_group(self, username, groupname):
        '''removes a user from a group
           returns true on success
           returns false on fail (user didnt exist, group didn't exist)'''
        debugprint('***ldap_remove_user_from_group*** : enter') 
        retval = False
        try:
            #get group
            gresult = self.ldap_query(base=self.GROUP_BASE, filter='(&(objectclass=groupofuniquenames) (cn=%s))' % groupname)
            gdn = gresult[0].get_dn()
            ud = self.ldap_get_user_details(username)
            if len(ud) == 0:
                debugprint('\tNo user found')
            else:
                #remove the user from the group
                udn = self.ldap_get_user_dn(username)
                debugprint('\tRemoving user %s from group %s' % (udn, gdn))
                old = gresult[0]
                oldattrs = old.get_attributes()
                import copy
                newattrs = copy.deepcopy(oldattrs)
                debugprint('\toldattrs: ', old.get_attributes())
                #catch code for empty groups (no 'uniquemmembers')
                if not newattrs.has_key('uniqueMember'):
                    newattrs['uniqueMember'] = []

                newattrs['uniqueMember'].remove(udn) 
                import ldap.modlist as modlist
                mods = modlist.modifyModlist(oldattrs, newattrs, ignore_oldexistent=1)
                debugprint('MODS:%s' % (str(mods)))
                if len(mods) > 0:
                    r = self.l.modify_ext_s(gdn, mods)
                retval = True
        except Exception, e:
            print 'Exception when removing %s from %s: %s' % (username, groupname, str(e)) 

        debugprint('***ldap_remove_user_from_group*** : exit')
        return retval

      
class LDAPBackend():
    def authenticate(self, username=None, password=None):
        
        user = None
        # anonymous bind to server
        ld = LDAPHandler()
        l = ld.l

        #
        # user test
        #
        userfilter = "(&(objectclass=person) (uid=%s))" % username
        result_data = ld.ldap_query(filter = userfilter, rattrs=['dn'])
        # If the user does not exist in LDAP, Fail.
        if (len(result_data) != 1):
            debugprint('User didnt exist')
            return None
        # Attempt to bind to the user's DN
        try:
            userdn = result_data[0].get_dn() #userDN of the first result
            l.simple_bind_s(userdn,password)
        except ldap.INVALID_CREDENTIALS, e:
            # Name or password were bad. Fail.
            print "Ldap Exception:\n%s" % e
            return None

        #
        # group membership test
        #
        groupfilter = '(&(objectClass=groupofuniquenames)(uniqueMember=%s)(cn=%s))' % (userdn, ld.GROUP)
        group_result_data = ld.ldap_query(filter=groupfilter, base=ld.GROUP_BASE, rattrs=['cn'])
        # If the group membership does not exist in LDAP, Fail.
        if (len(group_result_data) != 1):
            debugprint( 'Member of no groups' )
            return None
        #
        # The user existed and authenticated. Get the user
        # record or create one with no privileges.
        #
        #For Django's sake, replace @ and . with _ in the username
        #username = username.replace('.', '_')
        #username = username.replace('@', '_')
        try:
            user = User.objects.get(username__exact=username)
            user.is_staff = True
            user.is_superuser = True  #TODO don't do this
            user.save()
            
        except User.DoesNotExist:

            try:
                group = Group.objects.get(name__exact=settings.DEFAULT_GROUP)
            except Group.DoesNotExist, e:
                print "Ldap Exception: Group DoesNotExist: %s\n%s" % (settings.DEFAULT_GROUP, e)
                return None

            user = User.objects.create_user(username,"")
            user.groups.add(group)
            user.save()

        # Success.
        debugprint ("Login Success %s" % user)
        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
