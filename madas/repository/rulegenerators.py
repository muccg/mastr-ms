from madas.repository.models import RuleGenerator, RuleGeneratorStartBlock, RuleGeneratorSampleBlock, RuleGeneratorEndBlock, Component

from madas.users.MAUser import getMadasUser

def create_rule_generator(name, description, accessibility, user, node, startblockvars, sampleblockvars, endblockvars, **kwargs):

    newRG = RuleGenerator()
    newRG.name = name
    newRG.description = description
    #newRG.state = 
    newRG.accessibility = accessibility 
    #newRG.version = 
    #newRG.previous_version = 
    newRG.created_by = user
    newRG.node = getMadasUser(user.username).Nodes[0] 
    
    newRG.save()

    index = 0

    for stb in startblockvars:
        #create the start block
        newStartBlock = RuleGeneratorStartBlock()
        newStartBlock.rule_generator = newRG
        newStartBlock.index = index
        newStartBlock.count = stb['count']
        newStartBlock.component = Component.objects.get(id=stb['component'])
        newStartBlock.save()

    index = 0
    for sab in sampleblockvars:
        #create sample block
        newSampleBlock = RuleGeneratorSampleBlock()
        newSampleBlock.rule_generator = newRG
        newSampleBlock.index = index
        newSampleBlock.sample_count = 1 #todo - sample count passed through?
        newSampleBlock.count = sab['count']
        newSampleBlock.component = Component.objects.get(id=sab['component'])
        newSampleBlock.order = 0 #todo = no order passed through?
        newSampleBlock.save()

    index = 0
    for seb in endblockvars:
        newEndBlock = RuleGeneratorEndBlock()
        newEndBlock.rule_generator = newRG
        newEndBlock.index = index
        newEndBlock.count = seb['count']
        newEndBlock.component = Component.objects.get(id=seb['component'])
        newEndBlock.save()
    
def edit_rule_generator(id, user, **kwargs):
    ret = True
    try:
        candidateRG = RuleGenerator.objects.get(id=id)
        if kwargs.get('state', None) is not None:
            candidateRG.state = kwargs.get('state')
        candidateRG.save()
    except Exception, e:
        #couldnt find rulegen, or some other error.
        ret = False

    return ret

