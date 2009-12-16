from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from madas.repository.models import Experiment, ExperimentStatus, Organ, AnimalInfo, HumanInfo, PlantInfo, MicrobialInfo, Treatment,  BiologicalSource, SampleClass, UserInvolvementType, SampleTimeline, UserExperiment, OrganismType
from madas.m.models import Organisation, Formalquote
from django.utils import webhelpers
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import get_model
from json_util import makeJsonFriendly
from madas.utils import setRequestVars, jsonResponse


def create_object(request, model):

    #allow arbitrary insertion of any data object
    #but requiring certain defaults to defined, particularly for object references
    #in some cases, look up the value
    
    #get args and remove the id from it if it exists
    
    if request.GET:
        args = request.GET
    else:
        args = request.POST
       
    #create model object
    model_obj = get_model('repository', model)
    obj = model_obj()
       
    for key in args.keys():
        obj.__setattr__(key, args[key])

    obj.save()

    if model == 'experiment':
        uit, created = UserInvolvementType.objects.get_or_create(name='Principal Investigator')
        user = User.objects.get(username=request.user.username)
        ue = UserExperiment()
        ue.experiment=obj
        ue.type=uit
        ue.user=user
        ue.save()   
        #default source and organ
        source = BiologicalSource(experiment=obj)
        source.type_id=1
        source.save()
        organ = Organ(experiment=obj)
        organ.name='Unknown'
        organ.save() 
    
    if model == 'biologicalsource':
        return records(request, 'organism', 'id', obj.organism.id)
        
    if model == 'animal' or model == 'plant' or model == 'human':
        o = Organ(source=obj, name='Unknown')
        o.save()

    return records(request, model, 'id', obj.id)
    

def update_object(request, model, id):
    
    if request.GET:
        args = request.GET
    else:
        args = request.POST
       
    #fetch the object and update all values
    model_obj = get_model('repository', model) # try to get app name dynamically at some point
    params = {'id':id}
    rows = model_obj.objects.filter(**params)
    
    for row in rows:
        for key in args:
            row.__setattr__(key, args[key])
        row.save()

    return records(request, model, 'id', id)
    
    
def delete_object(request, model, id):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    #fetch the object and update all values
    model_obj = get_model('repository', model) # try to get app name dynamically at some point
    params = {'id':id}
    rows = model_obj.objects.filter(**params)
    
    rows.delete()

    return records(request, model, 'id', id)
    
    
def associate_object(request, model, association, parent_id, id):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    #fetch the object and update all values
    model_obj = get_model('repository', model) # try to get app name dynamically at some point
    params = {'id':parent_id}
    rows = model_obj.objects.filter(**params)
    
    assoc_model_obj = get_model('repository', association) # try to get app name dynamically at some point
    assoc_params = {'id':id}
    assoc_rows = assoc_model_obj.objects.filter(**assoc_params)

    if len(assoc_rows) > 0:
        assoc_item = assoc_rows[0]
        assoc_name = association + 's'
        
        for row in rows:
            current_set = row.__getattribute__(assoc_name)
            current_set.add(assoc_item)
            row.save()

    return records(request, model, 'id', parent_id)


def dissociate_object(request, model, association, parent_id, id):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    #fetch the object and update all values
    model_obj = get_model('repository', model) # try to get app name dynamically at some point
    params = {'id':parent_id}
    rows = model_obj.objects.filter(**params)
    
    assoc_name = association + 's'
    
    for row in rows:
        current_set = row.__getattribute__(assoc_name)
        found = current_set.filter(id=id)
        for obj in found:
            current_set.remove(obj)
        row.save()

    return records(request, model, 'id', parent_id)
    

def records(request, model, field, value):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    ### Authorisation Check ###
    authenticated = request.user.is_authenticated()   
    if not authenticated == True:
        return jsonResponse(request, [])
    ### End Authorisation Check ###

    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'root': 'rows',
                            'id': 'id',
                            'successProperty': 'success',
                            'fields': []
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)


    model_obj = get_model('repository', model) # try to get app name dynamically at some point
    params = {str(field):str(value)}
    rows = model_obj.objects.filter(**params) 

    # add fields to meta data
    for f in model_obj._meta.fields:
        output['metaData']['fields'].append({'name':f.name})

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        d = {}
        for f in model_obj._meta.fields:
            d[f.name] = f.value_from_object(row)
        output['rows'].append(d)


    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))


def populate_select(request, model=None, key=None, value=None, field=None, match=None):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    model_whitelist = {'organism': ['id', 'name', 'type'],
                       'organ': ['id', 'name', 'source_id', 'tissue', 'cell_type', 'subcellular_cell_type'],
                       'genotype': ['id', 'name'],
                       'gender': ['id', 'name'],
                       'animal': ['id', 'sex', 'sex__name', 'age', 'parental_line'],
                       'location': ['id', 'name'],
                       'origindetails': ['id', 'detailed_location', 'information'],
                       'treatmentvariation': ['id','name','treatment'],
                       'treatment': ['id','name','source','description','type'],
                       'treatmenttype': ['id','name'],
                       'user': ['id','username'],
                       'standardoperationprocedure' : ['id', 'label'],
                       'organismtype' : ['id','name'],
                       'userinvolvementtype' : ['id', 'name'],
                       'plant' : ['development_stage'],
                       'growthcondition' : ['id', 'greenhouse_id', 'greenhouse__name', 'detailed_location', 'lamp_details'],
                       'organisation': ['id', 'name'],
                       'sampleclass': ['id', 'class_id', 'experiment__id'],
                       'formalquote': ['id', 'toemail']
                       }


    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    main_content_function = "" # may need to change this

    if not authenticated or not authorized:
        output = select_widget_json(authenticated=authenticated,authorized=authorized,main_content_function=main_content_function,success=False,input=[])        
        return HttpResponse(output, status=401)
    

    try:

        if model not in model_whitelist.keys():
            raise ObjectDoesNotExist()

        if model == 'organisation':
            model_obj = get_model('m', 'organisation')
        elif model == 'user':
            model_obj = get_model('auth', 'user')
        elif model == 'formalquote':
            model_obj = get_model('m', 'formalquote')
        else:
            model_obj = get_model('repository', model)
        
        if field and match:
            params = {str(field):str(match)}
            rows = model_obj.objects.filter(**params)
        else:
            rows = model_obj.objects

        if key not in model_whitelist[model]:
            raise ObjectDoesNotExist("Field not allowed.")
        if value and value not in model_whitelist[model]:
            raise ObjectDoesNotExist("Field not allowed.")

        values = []

        if key and value:
            for item in rows.values(key, value).distinct():
                values.append({"key":item[key], "value":item[value]})
        elif key and not value:
            for item in rows.values(key).distinct():
                values.append({"key":item[key], "value":item[key]})
        else:
            raise ObjectDoesNotExist()
        
        output = select_widget_json(authenticated=authenticated,authorized=authorized,main_content_function=main_content_function,success=True,input=values)
        return HttpResponse(output)

        
    except ObjectDoesNotExist:
        output = select_widget_json(authenticated=authenticated,authorized=authorized,main_content_function=main_content_function,success=False,input=[])
        return HttpResponseNotFound(output)


def update_single_source(request, exp_id):

    args = request.REQUEST
    
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': []
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }
    
    e = Experiment.objects.get(id=exp_id)
    
    if e is None:
        output['success'] = False
    else:
        try:
            bs = BiologicalSource.objects.get(experiment=e)
        except ObjectDoesNotExist:
            bs = BiologicalSource(experiment=e)
        
        bs.type = OrganismType.objects.get(id=args['type'])
        bs.information = args['information']
        try:
            bs.ncbi_id = int(args['ncbi_id'])
        except:
            bs.ncbi_id = None
        #bs.label = args['label']
        bs.save()
        
        #process additional info
        if int(args['type']) == 1:
            #check for existing items
            if bs.microbialinfo_set.count() == 0:
                mi = MicrobialInfo()
                mi.genus = args['genus']
                mi.species = args['species']
                mi.culture_collection_id = args['culture']
                mi.media = args['media']
                mi.fermentation_vessel = args['vessel']
                mi.fermentation_mode = args['mode']
                try:
                    mi.innoculation_density = str(float(args['density']))
                except:
                    pass
                try:
                    mi.fermentation_volume = str(float(args['volume']))
                except:
                    pass
                try:
                    mi.temperature = str(float(args['temperature']))
                except:
                    pass
                try:
                    mi.agitation = str(float(args['agitation']))
                except:
                    pass
                try:
                    mi.ph = str(float(args['ph']))
                except:
                    pass
                mi.gas_type = args['gastype']
                try:
                    mi.gas_flow_rate = str(float(args['flowrate']))
                except:
                    pass
                mi.gas_delivery_method = args['delivery']
                mi.gas_delivery_method = args['delivery']
                
                bs.microbialinfo_set.add(mi)
            else:
                mi = bs.microbialinfo_set.all()[0]
                mi.genus = args['genus']
                mi.species = args['species']
                mi.culture_collection_id = args['culture']
                mi.media = args['media']
                mi.fermentation_vessel = args['vessel']
                mi.fermentation_mode = args['mode']
                try:
                    mi.innoculation_density = str(float(args['density']))
                except:
                    pass
                try:
                    mi.fermentation_volume = str(float(args['volume']))
                except:
                    pass
                try:
                    mi.temperature = str(float(args['temperature']))
                except:
                    pass
                try:
                    mi.agitation = str(float(args['agitation']))
                except:
                    pass
                try:
                    mi.ph = str(float(args['ph']))
                except:
                    pass
                mi.gas_type = args['gastype']
                try:
                    mi.gas_flow_rate = str(float(args['flowrate']))
                except:
                    pass
                mi.gas_delivery_method = args['delivery']
                
                mi.save()
        elif int(args['type']) == 2:
            if bs.plantinfo_set.count() == 0:
                pi = PlantInfo()
                pi.development_stage = args['development_stage']
                bs.plantinfo_set.add(pi)
            else:
                pi = bs.plantinfo_set.all()[0]
                pi.development_stage = args['development_stage']
                pi.save()
        elif int(args['type']) == 3:
            if bs.animalinfo_set.count() == 0:
                ai = AnimalInfo()
                ai.sex = args['sex']
                try:
                    ai.age = str(int(args['age']))
                except:
                    pass
                ai.parental_line = args['parental_line']
                ai.location = args['location']
                ai.notes = args['notes']
                bs.animalinfo_set.add(ai)
            else:
                ai = bs.animalinfo_set.all()[0]
                ai.sex = args['sex']
                try:
                    ai.age = str(int(args['age']))
                except:
                    pass
                ai.parental_line = args['parental_line']
                ai.location = args['location']
                ai.notes = args['notes']
                ai.save()
        elif int(args['type']) == 4:
            if bs.humaninfo_set.count() == 0:
                hi = HumanInfo()
                hi.sex = args['sex']
                hi.date_of_birth = args['date_of_birth']
                hi.bmi = args['bmi']
                hi.diagnosis = args['diagnosis']
                hi.location = args['location']
                hi.notes = args['notes']
                bs.humaninfo_set.add(hi)
            else:
                hi = bs.humaninfo_set.all()[0]
                hi.sex = args['sex']
                hi.date_of_birth = args['date_of_birth']
                hi.bmi = args['bmi']
                hi.diagnosis = args['diagnosis']
                hi.location = args['location']
                hi.notes = args['notes']
                hi.save()
    
    return HttpResponse(json.dumps(output))
    

def recreate_sample_classes(request, experiment_id):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    combos = []

    for biosource in BiologicalSource.objects.filter(experiment__id=experiment_id):
        zcombos = []
        for organ in Organ.objects.filter(experiment__id=experiment_id):
            acombos = []

            base = { 'bs': biosource.id, 'o': organ.id }
            bcombos = [base]

            newcombos = []
            for treatment in Treatment.objects.filter(experiment__id=experiment_id):
                for combo in bcombos:
                    tmp = combo.copy()
                    tmp['treatment'] = treatment.id
                    newcombos.append(tmp.copy())
            if len(newcombos) == 0:
                newcombos = bcombos[:]
                
            acombos = acombos + newcombos
            
            newcombos = []
            for timeline in SampleTimeline.objects.filter(experiment__id=experiment_id):
                for combo in acombos:
                    tmp = combo.copy()
                    tmp['time'] = timeline.id
                    newcombos.append(tmp.copy())
                acombos = newcombos[:]

            zcombos = zcombos + acombos
        
        combos = combos + zcombos
        
    #iterate over combos and current sampleclasses
    #if they already exist, fine
    #if they no longer exist, delete
    #if they don't exist, create
    currentsamples = SampleClass.objects.filter(biological_source__experiment__id = experiment_id)
    
    #determine what to delete and what to add
    foundclasses = set()
    for combo in combos:
        #look for item in currentsamples, if it exists, add it to the foundclasses set

        a = currentsamples
        
        #item for adding
        sc = SampleClass()
        sc.experiment_id = experiment_id
        sc.class_id = 'sample class'
        
        for key in combo.keys():
            if key == 'treatment':
                sc.treatments_id = combo[key]
                a = a.filter(treatments__id = combo[key])
            elif key == 'bs':
                sc.biological_source_id = combo[key]
                a = a.filter(biological_source__id = combo[key])
            elif key == 'o':
                sc.organ_id = combo[key]
                a = a.filter(organ__id = combo[key])
            elif key == 'time':
                sc.timeline_id = combo[key]
                a = a.filter(timeline__id = combo[key])

        if a:
            combo['id'] = a[0].id
            foundclasses.add(a[0].id)
        else:
            #if not found, add it on the spot
            sc.save()
            foundclasses.add(sc.id)

    #purge anything not in foundclasses
    purgeable = currentsamples.exclude(id__in=foundclasses)
    purgeable.delete()

    return recordsSampleClasses(request, experiment_id)


def recordsSampleClasses(request, experiment_id):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': [{'name':'id'}, {'name':'class_id'}, {'name':'treatment'}, {'name':'timeline'}, {'name':'organ'},  {'name':'enabled'}]
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)


    rows = SampleClass.objects.filter(experiment__id=experiment_id) 

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        d = {}
        d['id'] = row.id
        d['class_id'] = row.class_id
        d['enabled'] = row.enabled
        
        if row.treatments:
            d['treatment'] = row.treatments.name
        
        if row.timeline:
            d['timeline'] = str(row.timeline)
        else:
            d['timeline'] = ''
            
        if row.organ:
            d['organ'] = row.organ.name

        output['rows'].append(d)


    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))
    
    
def recordsExperiments(request):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': [{'name':'id'}, {'name':'status'}, {'name':'title'}, {'name':'job_number'}, {'name':'client'},  {'name':'principal'}, {'name':'description'}]
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)


    rows = Experiment.objects.all() 

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        d = {}
        d['id'] = row.id
        d['status'] = row.status.id
        d['title'] = row.title
        d['description'] = row.description
        d['job_number'] = row.job_number
        try:
            d['client'] = UserExperiment.objects.filter(type__id=3, experiment__id=row.id)[0].user.username
        except:
            d['client'] = ''
        try:
            d['principal'] = UserExperiment.objects.filter(type__id=1, experiment__id=row.id)[0].user.username
        except:
            d['principal'] = ''

        output['rows'].append(d)


    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))
    
    
def recordsSamples(request, experiment_id):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': [{'name':'id'}, {'name':'label'}, {'name':'weight'}, {'name':'comment'}, {'name':'sample_class'}, {'name':'last_status'}]
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)


    rows = Experiment.objects.get(id=experiment_id).sample_set.all()

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        d = {}
        d['id'] = row.id
        d['label'] = row.label
        d['weight'] = row.weight
        d['comment'] = row.comment
        d['sample_class'] = row.sample_class_id
        try:
            status = row.samplelog_set.all().order_by('-changetimestamp')[0]
            d['last_status'] = status.description
        except:
            d['last_status'] = ''

        output['rows'].append(d)


    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))
        

def moveFile(request):
    
    output = {'success':'', 'newlocation':''}
    
    if request.GET:
        args = request.GET
    else:
        args = request.POST
       
    target = args['target']
    file = args['file']
    
    exp = Experiment.objects.get(id=args['experiment_id'])
    exp.ensure_dir()
        
    import settings, os
    
    exppath = settings.REPO_FILES_ROOT + os.sep + 'experiments' + os.sep + str(exp.created_on.year) + os.sep + str(exp.created_on.month) + os.sep + str(exp.id) + os.sep
    pendingPath = settings.REPO_FILES_ROOT + os.sep + 'pending' + os.sep + file

    (path, filename) = os.path.split(pendingPath)
    
    destpath = exppath
    if not target == '':
        if not target == 'experimentRoot':
            destpath = destpath + target + os.sep
    
    #see if pendingpath exists
    if os.path.exists(pendingPath):
        os.rename(pendingPath, destpath + filename)
    
    output['success'] = True
    output['newlocation'] = exppath + filename
    
    return HttpResponse(json.dumps(output))

    
def experimentFilesList(request):
    
    if request.GET:
        args = request.GET
    else:
        args = request.POST

    path = args['node']
    
    if path == 'experimentRoot':
        path = ''
    
    if args['experiment'] == '0':
        return HttpResponse('[]')
        
    exp = Experiment.objects.get(id=args['experiment'])
    exp.ensure_dir()
        
    import settings, os
    
    exppath = settings.REPO_FILES_ROOT + os.sep + 'experiments' + os.sep + str(exp.created_on.year) + os.sep + str(exp.created_on.month) + os.sep + str(exp.id) + os.sep
    
    return _fileList(request, exppath, path)
    
    
def pendingFilesList(request):
    
    if request.GET:
        args = request.GET
    else:
        args = request.POST
        
    path = args['node']
    
    if path == 'pendingRoot':
        path = ''

    import settings, os
    
    basepath = settings.REPO_FILES_ROOT + os.sep + 'pending' + os.sep
    
    return _fileList(request, basepath, path)
    
    
def _fileList(request, basepath, path):

    import os

    output = []

    #verify that there is no up-pathing hack happening
    if len(os.path.abspath(basepath)) > len(os.path.commonprefix((basepath, os.path.abspath(basepath + path)))):
        return HttpResponse(json.dumps(output))

    if not os.path.exists(basepath + path):
        print 'error accessing path: ' + basepath + path
        return HttpResponse('[]')

    files = os.listdir(basepath + path)
    files.sort()
    
    for filename in files:
        filepath = basepath + filename
        if not path == '':
            filepath = basepath + path + os.sep + filename
            
        if os.access(filepath, os.R_OK):
            file = {}
            file['text'] = filename
            if os.path.isdir(filepath):
                file['leaf'] = False
            else:
                file['leaf'] = True
            file['id'] = filename
            if not path == '':
                file['id'] = path + os.sep + filename
            output.append(file)
        
    return HttpResponse(json.dumps(output))
    
    
def uploadFile(request):

    if request.GET:
        args = request.GET
    else:
        args = request.POST

    ############# FILE UPLOAD ########################
    output = { 'success': True }
    
    try:
        #TODO handle file uploads - check for error values
        print request.FILES.keys()
        if request.FILES.has_key('attachfile'):
            f = request.FILES['attachfile']
            print '\tuploaded file name: ', f._get_name()
            translated_name = f._get_name().replace(' ', '_')
            print '\ttranslated name: ', translated_name
            _handle_uploaded_file(f, translated_name)
            attachmentname = translated_name
        else:
            print '\tNo file attached.'
    except Exception, e:
        print '\tException: ', str(e)
        output = { 'success': False }
        
    return HttpResponse(json.dumps(output))
    
    
def _handle_uploaded_file(f, name):
    '''Handles a file upload to the projects WRITABLE_DIRECTORY
       Expects a django InMemoryUpload object, and a filename'''
    print '*** _handle_uploaded_file: enter ***'
    retval = False
    try:
        import os, settings
        
        destination = open(settings.REPO_FILES_ROOT + os.sep + 'pending' + os.sep + name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        retval = True
    except Exception, e:
        retval = False
        print '\tException in file upload: ', str(e)
    print '*** _handle_uploaded_file: exit ***'
    return retval
    
    
def sample_class_enable(request, id):
    
    if request.GET:
        args = request.GET
    else:
        args = request.POST

    sc = SampleClass.objects.get(id=id)
    
    if sc.enabled:
        sc.enabled = False
    else:
        sc.enabled = True
        
    sc.save()
        
    return recordsSampleClasses(request, sc.biological_source.experiment.id)

    
def select_widget_json(authenticated=False, authorized=False, main_content_function=None, success=False, input=""):

    output = {}
    output["authenticated"] = authenticated
    output["authorized"] = authorized

    output["response"] = {"value": {"items": input,
                                    "total_count":len(input),
                                    "version":1
                                    }}
    output["success"] = success
    return json.dumps(output)
