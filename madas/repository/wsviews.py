from django.db import transaction
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from madas.repository.models import Experiment, ExperimentStatus, Organ, AnimalInfo, HumanInfo, PlantInfo, MicrobialInfo, Treatment,  BiologicalSource, SampleClass, Sample, UserInvolvementType, SampleTimeline, UserExperiment, OrganismType, Project, SampleLog, Run, RunSample, InstrumentMethod, ClientFile
from madas.m.models import Organisation, Formalquote
from django.utils import webhelpers
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.db.models import get_model
from json_util import makeJsonFriendly
from madas.utils import setRequestVars, jsonResponse
from madas.repository.permissions import user_passes_test


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def create_object(request, model):
    '''
    Allow arbitrary insertion of any data object but requiring certain defaults
    to be defined, particularly for object references in some cases, look up the value
    '''

    # get args and remove the id from it if it exists
    if request.GET:
        args = request.GET
    else:
        args = request.POST
       
    #create model object
    model_obj = get_model('repository', model)
    obj = model_obj()
       
    for key in args.keys():
        obj.__setattr__(key, args[key])

    if model == 'run':
        obj.creator = User.objects.get(username=request.user.username)

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
        
    if model == 'samplelog':
        user = User.objects.get(username=request.user.username)
        obj.user = user
        obj.save()

    return records(request, model, 'id', obj.id)


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def create_samples(request):
    # get args and remove the id from it if it exists
    if request.GET:
        args = request.GET
    else:
        args = request.POST
       
    #create model object
    model_obj = get_model('repository', 'sample')
    
    for i in range(0, int(args['replicates'])):
        obj = model_obj()
           
        for key in args.keys():
            obj.__setattr__(key, args[key])
    
        obj.save()

    return records(request, 'sample', 'id', obj.id)
    

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def create_sample_log(request, sample_id, type, description):
    log = SampleLog(type=type,description=description,sample_id=sample_id)
    log.save()


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
@transaction.commit_on_success
def batch_create_sample_logs(request):
    #get args and remove the id from it if it exists
    if request.GET:
        args = request.GET
    else:
        args = request.POST

    #todo stuff
    type = args.get('type')
    description = args.get('description')
    sampleids = args.get('sample_ids').split(',')
    
    for sampleid in sampleids:
        create_sample_log(request, sampleid, type, description)
    return records(request, 'samplelog', 'id', 0)


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def update_object(request, model, id):
    
    if id == '0':
        return create_object(request, model)
    
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
    
    
@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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
    
    
@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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
    

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def records(request, model, field, value):

    if request.GET:
        args = request.GET
    else:
        args = request.POST

    ### TODO why do we need this, we'll get a 403 from decorator now if not logged in and not in group - ABM
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

    # TODO as above - do we need this now - ABM
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


def recordsClientFiles(request):

    if request.GET:
        args = request.GET
    else:
        args = request.POST

    ### TODO why do we need this, we'll get a 403 from decorator now if not logged in and not in group - ABM
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

    # TODO as above - do we need this now - ABM
    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)


    rows = ClientFile.objects.filter(experiment__users=request.user) 

    # add fields to meta data
    for f in ClientFile._meta.fields:
        output['metaData']['fields'].append({'name':f.name})
        try:
            f.rel.to
            output['metaData']['fields'].append({
                "name": f.name + "__unicode",
                "type": "string",
            })
        except AttributeError:
            pass

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        d = {}
        for f in ClientFile._meta.fields:
            d[f.name] = f.value_from_object(row)
            try:
                d[f.name + "__unicode"] = unicode(getattr(row, f.name))
            except:
                pass
            
        output['rows'].append(d)

    output = makeJsonFriendly(output)
    return HttpResponse(json.dumps(output))


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def populate_select(request, model=None, key=None, value=None, field=None, match=None):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    model_whitelist = {'organism': ['id', 'name', 'type'],
                       'organ': ['id', 'name', 'source_id', 'tissue', 'cell_type', 'subcellular_cell_type'],
                       'genotype': ['id', 'name'],
                       'gender': ['id', 'name'],
                       'animalinfo': ['id', 'sex', 'sex__name', 'age', 'parental_line'],
                       'location': ['id', 'name'],
                       'origindetails': ['id', 'detailed_location', 'information'],
                       'treatmentvariation': ['id','name','treatment'],
                       'treatment': ['id','name','source','description','type'],
                       'treatmenttype': ['id','name'],
                       'user': ['id','username'],
                       'standardoperationprocedure' : ['id', 'label'],
                       'organismtype' : ['id','name'],
                       'userinvolvementtype' : ['id', 'name'],
                       'plantinfo' : ['development_stage'],
                       'growthcondition' : ['id', 'greenhouse_id', 'greenhouse__name', 'detailed_location', 'lamp_details'],
                       'organisation': ['id', 'name'],
                       'sampleclass': ['id', 'class_id', 'experiment__id'],
                       'formalquote': ['id', 'toemail'],
                       'instrumentmethod': ['id','title'],
                       'machine': ['id','station_name']
                       }


    # TODO do we need this with the decorators in place? ABM
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
        elif model == 'machine':
            model_obj = get_model('mdatasync_server', 'nodeclient')
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


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def update_single_source(request, exp_id):

    args = request.GET.copy()
    
    for key in args.keys():
        if args[key] == '':
            args[key] = None
        if key == 'sex' and args[key] == '':
            args[key] = u'U'
    
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
#                ai.notes = args['notes']
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
#                ai.notes = args['notes']
                ai.save()
        elif int(args['type']) == 4:
            if bs.humaninfo_set.count() == 0:
                hi = HumanInfo()
                hi.sex = args['sex']
                hi.date_of_birth = args['date_of_birth']
                hi.bmi = args['bmi']
                hi.diagnosis = args['diagnosis']
                hi.location = args['location']
#                hi.notes = args['notes']
                bs.humaninfo_set.add(hi)
            else:
                hi = bs.humaninfo_set.all()[0]
                hi.sex = args['sex']
                hi.date_of_birth = args['date_of_birth']
                hi.bmi = args['bmi']
                hi.diagnosis = args['diagnosis']
                hi.location = args['location']
#                hi.notes = args['notes']
                hi.save()
    
    return HttpResponse(json.dumps(output))
    

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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
            sc = a[0]
        else:
            #if not found, add it on the spot
            sc.save()
            foundclasses.add(sc.id)
        #now check if we can auto-assign a name based on abbreviations
        if str(sc) != '':
            sc.class_id = str(sc)
            sc.save()

    #purge anything not in foundclasses
    purgeable = currentsamples.exclude(id__in=foundclasses)
    purgeable.delete()

    return recordsSampleClasses(request, experiment_id)


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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
                            'fields': [{'name':'id'}, {'name':'class_id'}, {'name':'treatment'}, {'name':'timeline'}, {'name':'organ'},  {'name':'enabled'}, {'name':'count'}]
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    # TODO do we need this with decorator in place ABM
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
        
        d['count'] = row.sample_set.count()

        output['rows'].append(d)


    output = makeJsonFriendly(output)
    return HttpResponse(json.dumps(output))
    

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def recordsExperiments(request):
   return recordsExperimentsForProject(request, None)


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def recordsExperimentsForProject(request, project_id):

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


    # Recreate the queryset filtering ExperimentAdmin does, since it's easier
    # than writing a custom serialiser for the Experiment model to fill in the
    # principal and client.
    if request.user.is_superuser:
        rows = Experiment.objects.all()
    else:
        rows = Experiment.objects.filter(users__id=request.user.id)
    
    if project_id is not None:
        rows = rows.filter(project__id=project_id)

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
    

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def recordsClients(request, *args):
    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': [{'name':'id'}, {'name':'client'}]
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    # TODO do we need this with decorator? ABM
    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)

    rows = User.objects.extra(where=["id IN (SELECT DISTINCT client_id FROM repository_project ORDER BY client_id)"])

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        output["rows"].append({
            "id": row.id,
            "client": row.username,
        })

    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)    
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
    # TODO do we need this ABM
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
            d['last_status'] = str(status)
        except:
            d['last_status'] = ''

        output['rows'].append(d)


    output = makeJsonFriendly(output)
    return HttpResponse(json.dumps(output))
    
    
@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def recordsSamplesForClient(request, client):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': [{'name':'id'}, {'name':'experiment_id'}, {'name':'experiment_title'}, {'name':'label'}, {'name':'weight'}, {'name':'comment'}, {'name':'sample_class'}, {'name':'last_status'}]
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    # TODO do we need this? ABM
    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)


    rows = Sample.objects.filter(experiment__users__username=client)

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
        d['experiment_id'] = row.experiment_id
        d['experiment_title'] = row.experiment.title
        try:
            status = row.samplelog_set.all().order_by('-changetimestamp')[0]
            d['last_status'] = str(status)
        except:
            d['last_status'] = ''

        output['rows'].append(d)


    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))
        

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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

    
@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def experimentFilesList(request):
    
    if request.GET:
        args = request.GET
    else:
        args = request.POST

    path = args['node']
    
    if path == 'experimentRoot':
        path = ''
    
    if not 'experiment' in args or args['experiment'] == '0':
        print 'invalid experiment'
        return HttpResponse('[]')
        
    exp = Experiment.objects.get(id=args['experiment'])
    exp.ensure_dir()
        
    import settings, os
    
    exppath = settings.REPO_FILES_ROOT + os.sep + 'experiments' + os.sep + str(exp.created_on.year) + os.sep + str(exp.created_on.month) + os.sep + str(exp.id) + os.sep
    
    sharedList = ClientFile.objects.filter(experiment=exp)
    print sharedList
    return _fileList(request, exppath, path, True, sharedList)
    

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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
    
    return _fileList(request, basepath, path, False, [])
    
    
@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def _fileList(request, basepath, path, withChecks, sharedList):

    import os

    output = []

    #verify that there is no up-pathing hack happening
    if len(os.path.abspath(basepath)) > len(os.path.commonprefix((basepath, os.path.abspath(basepath + path)))):
        print 'uppath problem for '+os.path.commonprefix((basepath, os.path.abspath(basepath + path)))
        return HttpResponse(json.dumps(output))

    if not os.path.exists(basepath + path):
        print 'error accessing path: ' + basepath + path
        return HttpResponse('[]')

    files = os.listdir(basepath + path)
    files.sort()
    
    print str(len(files)) + ' files in ' + basepath + path
    
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
            if withChecks:
                print 'checking'
                file['checked'] = False
                
                for cf in sharedList:
                    if file['id'] == cf.filepath:
                        file['checked'] = True
            output.append(file)
        
    return HttpResponse(json.dumps(output))

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def shareFile(request, *args):
    print 'shareFile:', str('')
    
    args = request.POST
    
    file = args['file']
    checked = args['checked']
    
    exp = Experiment.objects.get(id=args['experiment_id'])
    exp.ensure_dir()

    if checked == 'true':    
        try:
            client_file = ClientFile.objects.get(filepath=file, experiment=exp)
        except:
            client_file = ClientFile.objects.create(filepath=file, experiment=exp, sharedby=request.user)
        client_file.sharedby=request.user
        client_file.save()
    else:
        try:
            client_file = ClientFile.objects.get(filepath=file, experiment=exp)
            client_file.delete()
        except:
            pass
    
    return HttpResponse(json.dumps({'success':True}))
    
@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def downloadFile(request, *args):
    print 'downloadFile:', str('')
    
    args = request.REQUEST
    
    file = args['file']
    
    exp = Experiment.objects.get(id=args['experiment_id'])
    exp.ensure_dir()
    
    import os, settings
    filename = os.path.join(settings.REPO_FILES_ROOT, 'experiments', str(exp.created_on.year), str(exp.created_on.month), str(exp.id), file)
    from django.core.servers.basehttp import FileWrapper
    from django.http import HttpResponse

    from django.core.files import File
    wrapper = File(open(filename, "rb"))
    content_disposition = 'attachment;  filename=\"%s\"' % (str(file))
    response = HttpResponse(wrapper, content_type='application/download')
    response['Content-Disposition'] = content_disposition
    response['Content-Length'] = os.path.getsize(filename)
    return response 

def downloadClientFile(request, file_id):
    print 'downloadClientFile:', str('')

    try:
        cf = ClientFile.objects.get(id=file_id, experiment__users=request.user)
    except:
        return HttpResponseNotFound("You do not have permission to a file with that ID ("+file_id+")")
    
    exp = cf.experiment
    exp.ensure_dir()
    
    import os, settings
    filename = os.path.join(settings.REPO_FILES_ROOT, 'experiments', str(exp.created_on.year), str(exp.created_on.month), str(exp.id), cf.filepath)
    from django.core.servers.basehttp import FileWrapper
    from django.http import HttpResponse

    from django.core.files import File
    wrapper = File(open(filename, "rb"))
    content_disposition = 'attachment;  filename=\"%s\"' % (str(cf.filepath))
    response = HttpResponse(wrapper, content_type='application/download')
    response['Content-Disposition'] = content_disposition
    response['Content-Length'] = os.path.getsize(filename)
    return response 
    
@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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
    

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
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


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def generate_worklist(request,run_id):
    
    run = Run.objects.get(id=run_id)
    
    from runbuilder import RunBuilder
    
    rb = RunBuilder(run)
    
    #render
    # TODO set attribute on HttpResponse of content_type='application/download'
    return HttpResponse(rb.generate(request), content_type="text/plain")


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name="mastaff")) or False)
@transaction.commit_on_success
def mark_run_complete(request, run_id):
    samples = RunSample.objects.filter(run__id=run_id)
    
    for sample in samples:
        sample.complete = True
        sample.save()

    return HttpResponse(json.dumps({ "success": True }), content_type="text/plain")
    
    
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


@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def add_samples_to_run(request):
    '''Takes a run_id and a list of sample_ids and adds samples to the run after checking permissions etc.'''

    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    run_id = request.POST.get('run_id', None)
    if not run_id:
        return HttpResponseBadRequest("No run_id provided.\n")

    try:
        run = Run.objects.get(id=run_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Run with id %s not found.\n" % run_id)

    sample_id_str = request.POST.get('sample_ids', None)
    if not sample_id_str:
        return HttpResponseBadRequest("No sample_ids provided.\n")

    sample_ids = [int(X) for X in sample_id_str.split(',')]
    queryset = Sample.objects.filter(id__in=sample_ids)

    if len(queryset) != len(sample_ids):
        return HttpResponseNotFound("At least one of the samples can not be found.\n")

    # check that each sample is permitted
    samples = Sample.objects.filter(experiment__users=request.user)
    allowed_set = set(list(samples))
    qs_set = set(list(queryset))
    if not qs_set.issubset(allowed_set):
        return HttpResponseForbidden('Some samples do not belong to this user.\n')

    # check that each sample is valid
    for s in queryset:
        if not s.is_valid_for_run():
            return HttpResponseNotFound("Run NOT created as sample (%s, %s) does not have sample class or its class is not enabled.\n" % (s.label, s.experiment))

    # by the time you we get here we should have a valid run and valid samples
    run.add_samples(queryset)

    return HttpResponse()

@staff_member_required
@user_passes_test(lambda u: (u and u.groups.filter(name='mastaff')) or False)
def remove_samples_from_run(request):
    '''Takes a run_id and a list of sample_ids and remove samples from the run after checking permissions etc.'''

    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    run_id = request.POST.get('run_id', None)
    if not run_id:
        return HttpResponseBadRequest("No run_id provided.\n")

    try:
        run = Run.objects.get(id=run_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Run with id %s not found.\n" % run_id)

    sample_id_str = request.POST.get('sample_ids', None)
    if not sample_id_str:
        return HttpResponseBadRequest("No sample_ids provided.\n")

    sample_ids = [int(X) for X in sample_id_str.split(',')]
    queryset = Sample.objects.filter(id__in=sample_ids)

    # do it
    run.remove_samples(queryset)

    return HttpResponse()
