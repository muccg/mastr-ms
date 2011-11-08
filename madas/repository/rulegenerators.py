from madas.repository.models import RuleGenerator, RuleGeneratorStartBlock, RuleGeneratorSampleBlock, RuleGeneratorEndBlock, Component

from madas.users.MAUser import getMadasUser

def recreate_start_block(RG, startblockvars):
    # We will recreate the block by deleting the existing
    # block elements, but only after we know that all the new 
    # elements can be created
    newelements = []
    
    index=0
    for stb in startblockvars:
        #create the start block
        newStartBlock = RuleGeneratorStartBlock()
        newStartBlock.rule_generator = RG
        newStartBlock.index = index
        newStartBlock.count = stb['count']
        newStartBlock.component = Component.objects.get(id=stb['component'])
        newelements.append(newStartBlock)
        index+=1

    existing = RuleGeneratorStartBlock.objects.filter(rule_generator = RG)
    #delete existing
    for obj in existing:
        obj.delete()

    #add new
    for obj in newelements:
        obj.save()

def recreate_sample_block(RG, sampleblockvars):
    # We will recreate the block by deleting the existing
    # block elements, but only after we know that all the new 
    # elements can be created
    newelements = []
    index = 0
    for sab in sampleblockvars:
        #create sample block
        newSampleBlock = RuleGeneratorSampleBlock()
        newSampleBlock.rule_generator = RG
        newSampleBlock.index = index
        newSampleBlock.sample_count = sab['every'] 
        newSampleBlock.count = sab['count']
        newSampleBlock.component = Component.objects.get(id=sab['component'])
        newSampleBlock.order = sab['order'] 
        newelements.append(newSampleBlock)
        index+=1

    existing = RuleGeneratorSampleBlock.objects.filter(rule_generator = RG)
    for obj in existing:
        obj.delete()

    for obj in newelements:
        obj.save()
        
def recreate_end_block(RG, endblockvars):
    # We will recreate the block by deleting the existing
    # block elements, but only after we know that all the new 
    # elements can be created
    newelements = []
    
    index = 0
    for seb in endblockvars:
        newEndBlock = RuleGeneratorEndBlock()
        newEndBlock.rule_generator = RG
        newEndBlock.index = index
        newEndBlock.count = seb['count']
        newEndBlock.component = Component.objects.get(id=seb['component'])
        newelements.append(newEndBlock)
        index+=1

    #delete existing end block:
    existing = RuleGeneratorEndBlock.objects.filter(rule_generator = RG)
    for obj in existing:
        obj.delete()

    for obj in newelements:
        obj.save()


def create_rule_generator(name, description, accessibility, user, node, startblockvars, sampleblockvars, endblockvars, state=None, version=None, previous_version=None, **kwargs):

    success = False
    try:
        newRG = RuleGenerator()
        newRG.name = name
        newRG.description = description
        newRG.created_by = user
        newRG.node = getMadasUser(user.username).Nodes[0] 
        newRG.accessibility = accessibility 
        if state is not None:
            newRG.state = state
        if version is not None:
            newRG.version = version
        if previous_version is not None:
            newRG.previous_version = previous_version
        
        newRG.save()

        recreate_start_block(newRG, startblockvars)
        recreate_sample_block(newRG, sampleblockvars)
        recreate_end_block(newRG, endblockvars)
        success = True
    except Exception, e:
        print "Exception in create rule generator: %s" % ( e )
    
    return success


    
    
def edit_rule_generator(id, user, **kwargs):
    print "Edit rule generator: kwargs = ", kwargs
    ret = True
    try:
        candidateRG = RuleGenerator.objects.get(id=id)
        if kwargs.get('state', None) is not None:
            candidateRG.state = kwargs.get('state')
        if kwargs.get('accessibility', None) is not None:
            candidateRG.accessibility = kwargs.get('accessibility')
        if kwargs.get('version', None) is not None:
            candidateRG.version = kwargs.get('version')
        if kwargs.get('previous_version', None) is not None:
            candidateRG.version = kwargs.get('previous_version')
        if kwargs.get('name', None) is not None:
            candidateRG.name = kwargs.get('name')
        if kwargs.get('description', None) is not None:
            candidateRG.description = kwargs.get('description')
        print 'saving'
        candidateRG.save()
   
        if kwargs.get('startblock', None) is not None:
            recreate_start_block(candidateRG, kwargs.get('startblock'))
        if kwargs.get('sampleblock', None) is not None:
            recreate_sample_block(candidateRG, kwargs.get('sampleblock'))
        if kwargs.get('endblock', None) is not None:
            recreate_end_block(candidateRG, kwargs.get('endblock'))
    
    except Exception, e:
        print 'Exception: %s' % (e)
        #couldnt find rulegen, or some other error.
        ret = False

    return ret


def convert_to_dict(rulegenerator):
    d = {}
    d['id'] = rulegenerator.id
    d['name'] = rulegenerator.name
    d['version'] = rulegenerator.version
    d['full_name'] = rulegenerator.full_name
    d['description'] = rulegenerator.description
    d['state_id'] = rulegenerator.state
    d['state'] = rulegenerator.state_name
    d['accessibility_id'] = rulegenerator.accessibility
    d['accessibility'] = rulegenerator.accessibility_name
    d['created_by'] = unicode(rulegenerator.created_by)
    d['node'] = rulegenerator.node if rulegenerator.node else ''
    d['startblock'] = [{'count': r.count, 'component_id': r.component_id, 'component': r.component.sample_type} for r in rulegenerator.start_block_rules]
    d['sampleblock'] = [
        {
            'count': r.count, 
            'component_id': r.component_id,
            'component': r.component.sample_type, 
            'sample_count': r.sample_count,
            'order': r.order_name,
            'order_id' : r.order
        } for r in rulegenerator.sample_block_rules]
    d['endblock'] = [{'count': r.count, 'component_id': r.component_id, 'component': r.component.sample_type} for r in rulegenerator.end_block_rules]

    return d
