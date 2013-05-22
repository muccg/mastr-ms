from mastrms.repository.models import RuleGenerator, RuleGeneratorStartBlock, RuleGeneratorSampleBlock, RuleGeneratorEndBlock, Component
from mastrms.users.MAUser import MAUser

from mastrms.users.MAUser import getMadasUser
from django.db.models import Q

import logging
logger = logging.getLogger('madas_log')

def listRuleGenerators(user=None, accessibility=False, showEnabledOnly=False):
    logger.debug('Listing rule generators')
    usernode = None
    mauser = None
    if user is not None:
        mauser = getMadasUser(user.username)
        usernode = mauser.PrimaryNode

    rows = RuleGenerator.objects.all()

    apply_accessibility_node = Q(accessibility=RuleGenerator.ACCESSIBILITY_NODE) & Q(node=usernode)
    apply_accessibility_user = Q(created_by = user) & Q(accessibility=RuleGenerator.ACCESSIBILITY_USER)
    apply_accessibility_everyone = Q(accessibility=RuleGenerator.ACCESSIBILITY_ALL)
    apply_showonlyenabled = Q(state=RuleGenerator.STATE_ENABLED)


    #only bother doing accessibility if you arent an Admin or MA admin, and accessibility is true.
    if accessibility and (mauser is not None) and not mauser.IsAdmin and not mauser.IsMastrAdmin:
        rows = rows.filter(apply_accessibility_node | apply_accessibility_user | apply_accessibility_everyone)

    if showEnabledOnly:
        rows = rows.filter(apply_showonlyenabled)

    return rows

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

def create_rule_generator(name, description, accessibility, user, apply_sweep_rule, node, startblockvars, sampleblockvars, endblockvars, state=None, version=None, previous_version=None, **kwargs):
    '''Creates a new rule generator record and sets basic attributes.
       Then uses edit_rule_generator to set the blocks and state attributes'''
    success = False
    access = True
    message = ""
    try:
        newRG = RuleGenerator()
        newRG.name = name
        newRG.description = description
        newRG.created_by = user
        newRG.node = getMadasUser(user.username).PrimaryNode
        newRG.accessibility = accessibility
        #default state
        newRG.save()


        success, access, message = edit_rule_generator(newRG.id, user,
                                        apply_sweep_rule = apply_sweep_rule,
                                        startblock = startblockvars,
                                        sampleblock = sampleblockvars,
                                        endblock = endblockvars,
                                        state = state)
    except Exception, e:
        print "Exception in create rule generator: %s" % ( e )

    return success, access, message


def edit_rule_generator(id, user, **kwargs):
    '''Edits an existing rule generator. The
       functions which set the blocks (start, sample, end)
       will drop all current records and recreate with the
       newly submitted ones

       Any parameters coming through as None are ignored.
       '''
    success = False
    access = True
    message = ""

    try:
        candidateRG = RuleGenerator.objects.get(id=id)
        print "In edit, user = ", type(user)
        if candidateRG.is_accessible_by(user):

            if kwargs.get('apply_sweep_rule') is not None:
                candidateRG.apply_sweep_rule = kwargs.get('apply_sweep_rule')
            if kwargs.get('state') is not None:
                candidateRG.state = kwargs.get('state')
            if kwargs.get('accessibility') is not None:
                candidateRG.accessibility = kwargs.get('accessibility')
            if candidateRG.version is None:
                # Don't allow changing the name of a versioned RG
                if kwargs.get('name') is not None:
                    candidateRG.name = kwargs.get('name')
            if kwargs.get('description') is not None:
                candidateRG.description = kwargs.get('description')
            candidateRG.save()

            if kwargs.get('startblock', None) is not None:
                recreate_start_block(candidateRG, kwargs.get('startblock'))
            if kwargs.get('sampleblock', None) is not None:
                recreate_sample_block(candidateRG, kwargs.get('sampleblock'))
            if kwargs.get('endblock', None) is not None:
                recreate_end_block(candidateRG, kwargs.get('endblock'))

            success = True
        else:
            success = False
            access = False

    except Exception, e:
        print 'Exception: %s' % (e)
        #couldnt find rulegen, or some other error.
        success = False
        message = "Error editing rule generator details"

    return success, access, message

def copy_rules(sourceRG, destRG):
    for rule in sourceRG.start_block_rules:
        destRG.rulegeneratorstartblock_set.create(
                index = rule.index,
                count = rule.count,
                component = rule.component)
    for rule in sourceRG.sample_block_rules:
        destRG.rulegeneratorsampleblock_set.create(
                index = rule.index,
                sample_count = rule.sample_count,
                count = rule.count,
                component = rule.component,
                order = rule.order)
    for rule in sourceRG.end_block_rules:
        destRG.rulegeneratorendblock_set.create(
                index = rule.index,
                count = rule.count,
                component = rule.component)


def clone_rule_generator(rg_id, user):
    rg = RuleGenerator.objects.get(pk=rg_id)
    newRG = RuleGenerator.objects.create(
            name = 'CLONED - %s' % rg.name if not rg.name.startswith('CLONED') else rg.name,
            description = rg.description,
            accessibility = rg.accessibility,
            created_by = user,
            apply_sweep_rule = rg.apply_sweep_rule,
            node = getMadasUser(user.username).PrimaryNode
        )

    copy_rules(rg, newRG)
    return newRG.pk

def create_new_version_of_rule_generator(rg_id, user):
    rg = RuleGenerator.objects.get(pk=rg_id)
    if rg.version is None:
        rg.version = 1
        rg.save()

    newRG = RuleGenerator.objects.create(
            name = rg.name,
            version = rg.version+1,
            description = rg.description,
            accessibility = rg.accessibility,
            previous_version = rg,
            created_by = user,
            apply_sweep_rule = rg.apply_sweep_rule,
            node = getMadasUser(user.username).PrimaryNode
        )

    copy_rules(rg, newRG)
    return newRG.pk


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
    d['apply_sweep_rule_display'] = 'Yes' if rulegenerator.apply_sweep_rule else 'No'
    d['apply_sweep_rule'] = rulegenerator.apply_sweep_rule
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
