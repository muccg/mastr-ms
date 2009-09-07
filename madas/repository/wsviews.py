from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from madas.repository.models import Experiment, ExperimentStatus, Organism, Organ, Genotype, Gender, Animal, Location, OriginDetails, TreatmentVariation, Treatment, StandardOperationProcedureCategory , BiologicalSource, SampleClass, GrowthCondition, UserInvolvementType, UserExperiment
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
    args = request.GET

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
    
    if model == 'biologicalsource':
        return records(request, 'organism', 'id', obj.organism.id)
        
    if model == 'animal' or model == 'plant' or model == 'human':
        o = Organ(source=obj, name='Unknown')
        o.save()
        
    if model == 'treatment':
        #create a variation immediately
        tv = TreatmentVariation(name='standard', treatment=obj);
        tv.save()

    return records(request, model, 'id', obj.id)
    

def update_object(request, model, id):

    #fetch the object and update all values
    model_obj = get_model('repository', model) # try to get app name dynamically at some point
    params = {'id':id}
    rows = model_obj.objects.filter(**params)
    
    args = request.GET
    
    for row in rows:
        for key in args:
            row.__setattr__(key, args[key])
        row.save()

    return records(request, model, 'id', id)
    
    
def delete_object(request, model, id):

    #fetch the object and update all values
    model_obj = get_model('repository', model) # try to get app name dynamically at some point
    params = {'id':id}
    rows = model_obj.objects.filter(**params)
    
    args = request.GET
    
    rows.delete()

    return records(request, model, 'id', id)
    
    
def associate_object(request, model, association, parent_id, id):

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
                       'lamptype': ['id', 'name']
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

        if model == 'user':
            model_obj = get_model('auth', 'user')
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


def recreate_sample_classes(request, experiment_id):

    combos = []

    for biosource in BiologicalSource.objects.filter(experiment__id=experiment_id):
        zcombos = []
        for organ in biosource.organ_set.all():
            acombos = []

            base = { 'bs': biosource.id, 'o': organ.id }
            bcombos = [base]

            newcombos = []
            for treatment in biosource.treatment_set.all():
                if treatment.treatmentvariation_set.all():
                    for variation in treatment.treatmentvariation_set.all():
                        for combo in bcombos:
                            tmp = combo.copy()
                            tmp['var'] = variation.id
                            newcombos.append(tmp.copy())
            if len(newcombos) == 0:
                newcombos = bcombos[:]
                
            acombos = acombos + newcombos
            
            newcombos = []
            for timeline in biosource.sampletimeline_set.all():
                for combo in acombos:
                    tmp = combo.copy()
                    tmp['time'] = timeline.id
                    newcombos.append(tmp.copy())
                acombos = newcombos[:]

            newcombos = []
            if len(biosource.origin_set.all()) > 0:
                for origin in biosource.origin_set.all():
                    for combo in acombos:
                        tmp = combo.copy()
                        tmp['origin'] = origin.id
                        newcombos.append(tmp.copy())

                acombos = newcombos[:]

            newcombos = []
            for genotype in biosource.genotype_set.all():
                for combo in acombos:
                    tmp = combo.copy()
                    tmp['geno'] = genotype.id
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
        sc.class_id = 'sample class'
        
        for key in combo.keys():
            if key == 'var':
                sc.treatments_id = combo[key]
                a = a.filter(treatments__id = combo[key])
            elif key == 'geno':
                sc.genotype_id = combo[key]
                a = a.filter(genotype__id = combo[key])
            elif key == 'bs':
                sc.biological_source_id = combo[key]
                a = a.filter(biological_source__id = combo[key])
            elif key == 'o':
                sc.organ_id = combo[key]
                a = a.filter(organ__id = combo[key])
            elif key == 'time':
                sc.timeline_id = combo[key]
                a = a.filter(timeline__id = combo[key])
            elif key == 'origin':
                sc.origin_id = combo[key]
                a = a.filter(origin__id = combo[key])

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

    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': [{'name':'id'}, {'name':'class_id'}, {'name':'treatments'}, {'name':'timeline'}, {'name':'origin'}, {'name':'organ'}, {'name':'genotype'}, {'name':'enabled'}]
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


    rows = SampleClass.objects.filter(biological_source__experiment__id=experiment_id) 

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        d = {}
        d['id'] = row.id
        d['class_id'] = row.class_id
        d['enabled'] = row.enabled
        
        if row.treatments:
            d['treatments'] = row.treatments.name
        
        if row.timeline:
            d['timeline'] = str(row.timeline)
        else:
            d['timeline'] = ''
            
        if row.origin:
            d['origin_id'] = row.origin.id
            
            if GrowthCondition.objects.filter(id=row.origin.id):
                d['origin'] = GrowthCondition.objects.get(id=row.origin.id).detailed_location
            if OriginDetails.objects.filter(id=row.origin.id):
                d['origin'] = OriginDetails.objects.get(id=row.origin.id).detailed_location    
        
        if row.organ:
            d['organ'] = row.organ.name
        
        if row.genotype:
            d['genotype'] = row.genotype.name
            
        output['rows'].append(d)


    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))
    

def moveFile(request):
    
    output = {'success':'', 'newlocation':''}
    
    args = request.GET
    target = args['target']
    file = args['file']
    
    exp = Experiment.objects.get(id=args['experiment_id'])
    exp.ensure_dir()
        
    import settings, os
    
    exppath = settings.REPO_FILES_ROOT + 'experiments' + os.sep + str(exp.created_on.year) + os.sep + str(exp.created_on.month) + os.sep + str(exp.id) + os.sep
    pendingPath = settings.REPO_FILES_ROOT + 'pending' + os.sep + file

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
    
    args = request.GET
    path = args['node']
    
    if path == 'experimentRoot':
        path = ''
    
    if args['experiment'] == '0':
        return HttpResponse('[]')
        
    exp = Experiment.objects.get(id=args['experiment'])
    exp.ensure_dir()
        
    import settings, os
    
    exppath = settings.REPO_FILES_ROOT + 'experiments' + os.sep + str(exp.created_on.year) + os.sep + str(exp.created_on.month) + os.sep + str(exp.id) + os.sep
    
    return _fileList(request, exppath, path)
    
    
def pendingFilesList(request):
    
    args = request.GET
    path = args['node']
    
    if path == 'pendingRoot':
        path = ''

    import settings, os
    
    basepath = settings.REPO_FILES_ROOT + 'pending' + os.sep
    
    return _fileList(request, basepath, path)
    
    
def _fileList(request, basepath, path):

    import os

    output = []

    #verify that there is no up-pathing hack happening
    if len(os.path.abspath(basepath)) > len(os.path.commonprefix((basepath, os.path.abspath(basepath + path)))):
        return HttpResponse(json.dumps(output))

    if not os.path.exists(basepath + path):
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
