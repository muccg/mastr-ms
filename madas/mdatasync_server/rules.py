class ActionType:
    EXCLUDE = 1
    INCLUDE = 2
    UPDATE_EXISTING = 4
    MOVE = 8
    ValidTypes = [EXCLUDE, INCLUDE, UPDATE_EXISTING, MOVE]
    #Any spaces needed in the command need to be in these strings.
    #They are joined to their arguments with no spaces
    CommandLookup = {
                        EXCLUDE : '--exclude=',
                        INCLUDE : '--include=',
                        UPDATE_EXISTING : '--existing ',
                        MOVE : '--noop',
                    }

class FileRule(object):
    '''FileRules take a target pattern, and an action.
       The patterns are standard regular expressions,
       The actions are:
       exclude
       include
       update_existing
    '''
    

    def __init__(self, tpattern, action):
        self.tpattern = tpattern
        if action not in ActionType.ValidTypes:
            print 'Invalid action: ', action
            return None
        else:
            self.action = action


    def toString(self):
        #find which action 
        if self.action is not ActionType.MOVE:
            return ('%s%s' % (ActionType.CommandLookup[self.action], self.tpattern) )
        else:
            return None

class NodeConfig(object):
    def __init__(self):
        self.nodes = {}

    def AddOrganisation(self, orgname):
        if self.nodes.has_key(org):
            print "AddOrganisation: warning: node name already existed."
        self.nodes[orgname] = {}

    def AddSite(self, orgname, sitename):
        if not self.nodes.has_key(orgname):
            pass #incomplete code, abandoned class

    def AddStation(self, orgname, sitename, stationname):
        if not self.nodes.has_key(nodename):
            print 'AddStation: warning: needed to create node ', nodename
        if not self.nodes[nodename].has_key(stationname):
            self.nodes[nodename][stationname] = [] 



    def AddRule(self, nodename, stationname, ruletarget, ruleaction):
        #first try to create the rule.
        r = FileRule(ruletarget, ruleaction)
        if r is not None:
        
            if not self.nodes.has_key(nodename):
                self.AddNode(nodename)
            if not self.nodes[nodename].has_key(stationname):
                self.AddStation(nodename, stationname)
            self.nodes[nodename][stationname].append("%s" % (r.toString()) )

    def toDict(self):
        return self.nodes

