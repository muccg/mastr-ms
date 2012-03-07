# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time
from quote.models import Organisation, Formalquote
from mdatasync_server.models import NodeClient
import grp
from mastrms.users.MAUser import getMadasUser
from django.core.files.storage import FileSystemStorage
import os
from mastrms import settings
from utils.file_utils import ensure_repo_filestore_dir_with_owner, set_repo_file_ownerships

class SampleNotInClassException(Exception):
    pass

class NotAuthorizedError(StandardError):
    pass

class MadasUser(User):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        User.__init__(self, *args, **kwargs)
        self.magroups = None

    def set_magroups(self, groups):
        if groups is None: groups = tuple()
        self.magroups = groups
        
    @property
    def is_admin(self):
        assert self.magroups is not None, "Groups not set"
        return ('Administrators' in self.magroups)

    @property
    def is_noderep(self):
        assert self.magroups is not None, "Groups not set"
        return ('Node Reps' in self.magroups)

    @property
    def is_client(self):
        assert self.magroups is not None, "Groups not set"
        return len(self.magroups) == 0

    def is_project_manager_of(self, project):
        return self.pk in [m.pk for m in project.managers.all()]
        
    def is_client_of(self, project):
        return (project.client and self.pk == project.client.pk)

class OrganismType(models.Model):
    """Currently, Microorganism, Plant, Animal or Human"""
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

       
class BiologicalSource(models.Model):
    experiment = models.ForeignKey('Experiment')
    abbreviation = models.CharField(max_length=5)
    type = models.ForeignKey(OrganismType)
    information = models.TextField(null=True, blank=True)
    ncbi_id = models.PositiveIntegerField(null=True, blank=True)
    label = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return ("%s %s %s %s" % (self.abbreviation, self.type, self.ncbi_id, self.label)).replace('None', '--')
    
class AnimalInfo(models.Model):
    class Meta:
        verbose_name_plural = "Animal information"

    source = models.ForeignKey(BiologicalSource)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'Unknown')
    )
    sex = models.CharField(max_length=2, choices=GENDER_CHOICES, default=u'U')
    age = models.PositiveIntegerField(null=True, blank=True)
    parental_line = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.sex, str(self.age), self.parental_line)

class PlantInfo(models.Model):
    class Meta:
        verbose_name_plural = "Plant information"

    source = models.ForeignKey(BiologicalSource)
    development_stage = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    growing_place = models.CharField(max_length=255, null=True, blank=True)
    seeded_on = models.DateField(null=True, blank=True)
    transplated_on = models.DateField(null=True, blank=True)
    harvested_on = models.DateField(null=True, blank=True)
    harvested_at = models.TimeField(null=True, blank=True)
    night_temp_cels = models.PositiveIntegerField(null=True, blank=True)
    day_temp_cels = models.PositiveIntegerField(null=True, blank=True)
    light_hrs_per_day = models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)
    light_fluence = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    light_source = models.TextField(null=True, blank=True)
    lamp_details = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s - %s" % (self.development_stage, self.growing_place)

class HumanInfo(models.Model):
    source = models.ForeignKey(BiologicalSource)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'Unknown')
    )
    sex = models.CharField(null=True, max_length=2, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.sex, self.date_of_birth, self.location)

class MicrobialInfo(models.Model):
    source = models.ForeignKey(BiologicalSource)
    genus = models.CharField(max_length=255, null=True, blank=True)
    species = models.CharField(max_length=255, null=True, blank=True)
    culture_collection_id = models.CharField(max_length=255, null=True, blank=True)
    media = models.CharField(max_length=255, null=True, blank=True)
    fermentation_vessel = models.CharField(max_length=255, null=True, blank=True)
    fermentation_mode = models.CharField(max_length=255, null=True, blank=True)
    innoculation_density = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fermentation_volume = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    agitation = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ph = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    gas_type = models.CharField(max_length=255, null=True, blank=True)
    gas_flow_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    gas_delivery_method = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"%s - %s" % (self.genus, self.species)

class Organ(models.Model):
    experiment = models.ForeignKey('Experiment')
    name = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=5)
    detail = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

class ExperimentStatus(models.Model):
    class Meta:
        verbose_name_plural = "Experiment statuses"

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateField(null=False, default=date.today)
    client = models.ForeignKey(User, null=True, blank=True)    
    managers = models.ManyToManyField(User, related_name='managed_projects')
    
    def __unicode__(self):
        client_username = 'No client'
        if self.client:
            client_username = self.client.username
        return "%s (%s)" % (self.title, client_username)

class InstrumentMethod(models.Model):
    title = models.CharField(max_length=255)
    method_path = models.TextField()
    method_name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    created_on = models.DateField(null=False, default=date.today)
    creator = models.ForeignKey(User, null=True)
    template = models.TextField()
    randomisation = models.BooleanField(default=False)
    blank_at_start = models.BooleanField(default=False)
    blank_at_end = models.BooleanField(default=False)
    blank_position = models.CharField(max_length=255,null=True,blank=True)
    obsolete = models.BooleanField(default=False)
    obsolescence_date = models.DateField(null=True,blank=True)
    
    #future: quality control sample locations

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.version) 
        
class Experiment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, through='UserExperiment', null=True, blank=True)
    status = models.ForeignKey(ExperimentStatus, null=True, blank=True)
    created_on = models.DateField(null=False, default=date.today)
    formal_quote = models.ForeignKey(Formalquote, null=True, blank=True)
    job_number = models.CharField(max_length=30)
    project = models.ForeignKey(Project)
    instrument_method = models.ForeignKey(InstrumentMethod, null=True, blank=True)
    sample_preparation_notes = models.TextField(null=True, blank=True)
    # ? files

    @property
    def experiment_dir(self):
        return os.path.join(settings.REPO_FILES_ROOT, self.experiment_reldir)

    @property
    def experiment_reldir(self):
        yearpath = os.path.join('experiments', str(self.created_on.year) )
        monthpath = os.path.join(yearpath, str(self.created_on.month) )
        exppath = os.path.join(monthpath, str(self.id) )
        return exppath


    def ensure_dir(self):
        ''' This function calculates where the storage area should be for the experiment data.
            It create the directory if it does not exist.
            It returns a tuple in form (abspath, relpath) where 
                abspath is the absolute path
                relpath is the path, relative to the settings.REPO_FILES_ROOT
        '''
        import stat
        
        yearpath = os.path.join('experiments', str(self.created_on.year) )
        monthpath = os.path.join(yearpath, str(self.created_on.month) )
        exppath = os.path.join(monthpath, str(self.id) )
       
        try:
            ensure_repo_filestore_dir_with_owner(exppath)
        except Exception, e:
            print "ensure dir exception: ", e
        return (abspath, exppath)


    def __unicode__(self):
        return self.title

sopdir = 'sops'
sopfs = FileSystemStorage(location=os.path.join(settings.REPO_FILES_ROOT, sopdir))

class StandardOperationProcedure(models.Model):
    responsible = models.CharField(max_length=255, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    area_where_valid = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    organisation = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    defined_by = models.CharField(max_length=255, null=True, blank=True)
    replaces_document = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)

    def _filepath(self, filename):
        ensure_repo_filestore_dir_with_owner(sopdir)
        return os.path.join(sopfs.location, self.version, filename)


    attached_pdf = models.FileField(storage=sopfs, upload_to=_filepath, null=True, blank=True, max_length=500)
    experiments = models.ManyToManyField(Experiment, null=True, blank=True)
    
    def __unicode__(self):
        return self.label

class Treatment(models.Model):
    experiment = models.ForeignKey('Experiment')
    abbreviation = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class SampleTimeline(models.Model):
    experiment = models.ForeignKey('Experiment')
    abbreviation = models.CharField(max_length=5)
    timeline = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        if self.timeline == None:
            return ""
        return self.timeline

class SampleClass(models.Model):
    class Meta:
        verbose_name_plural = "Sample classes"

    class_id = models.CharField(max_length=255)
    experiment = models.ForeignKey(Experiment)
    biological_source = models.ForeignKey(BiologicalSource, null=True, blank=True)
    treatments = models.ForeignKey(Treatment, null=True, blank=True)
    timeline = models.ForeignKey(SampleTimeline,null=True, blank=True)
    organ = models.ForeignKey(Organ, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        val = ''
        if self.biological_source is not None:
            if self.biological_source.abbreviation is not None:
                val = val + self.biological_source.abbreviation
        if self.organ is not None:
            if self.organ.abbreviation is not None:
                val = val + self.organ.abbreviation
        if self.timeline is not None:
            if self.timeline.abbreviation is not None:
                val = val + self.timeline.abbreviation
        if self.treatments is not None:
            if self.treatments.abbreviation is not None:
                val = val + self.treatments.abbreviation
        if val == '':
            val = 'class_' + str(self.id)
        return val

class Sample(models.Model):
    sample_id = models.CharField(max_length=255)
    sample_class = models.ForeignKey(SampleClass, null=True, blank=True)
    experiment = models.ForeignKey(Experiment)
    label = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    sample_class_sequence = models.SmallIntegerField(default=1, db_index=True)

    def __unicode__(self):
        return u"%s-%s" % (self.sample_class.class_id, self.sample_class_sequence)

    def run_filename(self, run):
        if self.sample_class is None:
            raise SampleNotInClassException
        else:
            result = u"%s-%s" % (self.sample_class.class_id, self.sample_class_sequence)
            if self.label:
                result += "-%s" % self.label
            result += "_%s-%s" % (run.id, str(self.id))
            return result

    def is_valid_for_run(self):
        '''Test to determine whether this sample can be used in a run'''
        if not self.sample_class or not self.sample_class.enabled:
            return False
        return True


class RUN_STATES:
    NEW = (0, u"New")
    IN_PROGRESS = (1, u"In Progress")
    COMPLETE = (2, u"Complete")

    @staticmethod
    def name(state_id):
        for x in (RUN_STATES.NEW, RUN_STATES.IN_PROGRESS, RUN_STATES.COMPLETE):
            if x[0] == state_id:
                return x[1]
        return ''
        

class Run(models.Model):
    
    RUN_STATES_TUPLES = (
        RUN_STATES.NEW,
        RUN_STATES.IN_PROGRESS,
        RUN_STATES.COMPLETE)

    METHOD_ORDERS = (
        (1, 'resampled vial'),
        (2, 'individual vial')
    )   

    experiment = models.ForeignKey(Experiment, null=True)

    method = models.ForeignKey(InstrumentMethod)
    created_on = models.DateField(null=False, default=date.today)
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=255,null=True,blank=True)
    samples = models.ManyToManyField(Sample, through="RunSample")
    machine = models.ForeignKey(NodeClient, null=True, blank=True)
    generated_output = models.TextField(null=True, blank=True)
    state = models.SmallIntegerField(choices=RUN_STATES_TUPLES, default=0, db_index=True)
    sample_count = models.IntegerField(default=0)
    incomplete_sample_count = models.IntegerField(default=0)
    complete_sample_count = models.IntegerField(default=0)
    rule_generator = models.ForeignKey('RuleGenerator')
    number_of_methods = models.IntegerField(null=True, blank=True)
    order_of_methods = models.IntegerField(choices=METHOD_ORDERS, null=True, blank=True)

    
    def sortedSamples(self):
        #TODO if method indicates randomisation and blanks, now is when we would do it
        return self.samples.distinct()
    
    def __unicode__(self):
        return "%s (%s v.%s)" % (self.title, self.method.title, self.method.version)

    def resequence_samples(self):
        sequence = 1
        for rs in RunSample.objects.all().order_by("id"):
            rs.sequence = sequence
            sequence += 1
            rs.save()

    def add_samples(self, sampleslist):
        '''Takes a list of samples'''
        assert self.id, 'Run must have an id before samples can be added'
        for s in sampleslist:
            if s.is_valid_for_run():
                print 'add_samples adding ', s.id
                rs, created = RunSample.objects.get_or_create(run=self, sample=s)
        self.resequence_samples()
                
    def remove_samples(self, queryset):
        assert self.id, 'Run must have an id before samples can be added'
        for s in queryset:
            RunSample.objects.filter(run=self, sample=s).delete()
        self.resequence_samples()

    def update_sample_counts(self):
        qs = RunSample.objects.filter(run=self)

        self.sample_count = qs.count()
        self.incomplete_sample_count = qs.filter(complete=False).count()
        self.complete_sample_count = self.sample_count - self.incomplete_sample_count

        if self.complete_sample_count == self.sample_count:
            self.state = RUN_STATES.COMPLETE[0] 

        self.save()
        
    def ensure_dir(self):
        ''' This function calculates where the storage area should be for the run data (blanks and QC files)
            It create the directory if it does not exist.
            It returns a tuple in form (abspath, relpath) where 
                abspath is the absolute path
                relpath is the path, relative to the settings.REPO_FILES_ROOT
        '''
        import stat
        
        yearpath = os.path.join('runs', str(self.created_on.year) )
        monthpath = os.path.join(yearpath, str(self.created_on.month) )
        runpath = os.path.join(monthpath, str(self.id) )
       
        ensure_repo_filestore_dir_with_owner(runpath)

        return (abspath, runpath)
    
    def is_method_type_individual_vial(self):
        return (self.order_of_methods == 2)
 
class SampleLog(models.Model):
    LOG_TYPES = (
            (0, u'Received'),
            (1, u'Stored'),
            (2, u'Prepared'),
            (3, u'Acquired'),
            (4, u'Data Processed')
        )
    type = models.PositiveIntegerField(choices=LOG_TYPES, default=0)
    changetimestamp = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True)
    sample = models.ForeignKey(Sample)
    
    def __unicode__(self):
        return "%s: %s" % (self.LOG_TYPES[self.type][1], self.description)

class UserInvolvementType(models.Model):
    """Principal Investigator or Involved User"""
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class UserExperiment(models.Model):
    user = models.ForeignKey(User)
    experiment = models.ForeignKey(Experiment)
    type = models.ForeignKey(UserInvolvementType)
    additional_info = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s-%s" % (self.user, self.experiment)

class RunSample(models.Model):
    # TODO 
    SWEEP_ID = 6
    run = models.ForeignKey(Run)
    sample = models.ForeignKey(Sample, null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)
    complete = models.BooleanField(default=False, db_index=True)
    component = models.ForeignKey("Component", default=0)
    sequence = models.PositiveIntegerField(null=False, default=0)
    vial_number = models.PositiveIntegerField(null=True)
    method_number = models.PositiveIntegerField(null=True, blank=True)

    @classmethod 
    def create_sweep(self, run):
        return RunSample.objects.create(run=run, component_id=RunSample.SWEEP_ID)

    @classmethod 
    def create(self, run, component):
        return RunSample.objects.create(run=run, component=component)

    @classmethod 
    def create_copy(self, source, method_number=None):
        return RunSample.objects.create(run=source.run, component=source.component, sample=source.sample, method_number=method_number)
 
    class Meta:
        db_table = u'repository_run_samples'

    def __unicode__(self):
        return "Run: %s, Sample: %s, Filename: %s." % (self.run, self.sample, self.filename)

    def delete(self, *args, **kwargs):
        run = self.run
        super(RunSample, self).delete(*args, **kwargs)
        run.update_sample_counts()

    def save(self, *args, **kwargs):
        super(RunSample, self).save(*args, **kwargs)
        self.run.update_sample_counts()
        
    def filepaths(self):
        if self.is_sample():
            return self.sample.experiment.ensure_dir()
        else:
            return self.run.ensure_dir()

    def run_filename(self):
        filename = self.sample.run_filename(self.run)
        if self.method_number:
            filename += '_m%d' % self.method_number
        filename += '.d'
        return filename
            
    def generate_filename(self):
        if self.is_sample():
            return self.run_filename()
        else:
            return "%s_%s-%s.d"  % (self.component.filename_prefix, self.run.id, self.id)
            
    def get_sample_name(self):
        #for now, just return the filename without the .d suffix
        #this is a poor implementation
        #TODO better implementation
        return self.filename[:-2]
        
    sample_name = property(get_sample_name, None)
        
    def is_sample(self):
        return self.component_id == 0

    def is_blank(self):
        return self.component.component_group.name == 'Blank'

       
class ClientFile(models.Model):
    experiment = models.ForeignKey(Experiment)
    filepath = models.TextField()
    downloaded = models.BooleanField(default=False, db_index=True)
    sharetimestamp = models.DateTimeField(auto_now=True)
    sharedby = models.ForeignKey(User)

class InstrumentSOP(models.Model):
    title = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    split_threshhold = models.PositiveIntegerField(default=20)
    split_size = models.PositiveIntegerField(default=10)
    vials_per_tray = models.PositiveIntegerField(default=98)
    trays_max = models.PositiveIntegerField(default=1)
  
class ComponentGroup(models.Model):
    name = models.CharField(max_length=50) 

    def __unicode__(self):
        return self.name

class Component(models.Model):
    sample_type = models.CharField(max_length=255)
    sample_code = models.CharField(max_length=255)
    component_group = models.ForeignKey(ComponentGroup)
    filename_prefix = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s (%s)" % (self.sample_type, self.sample_code)

class RuleGenerator(models.Model):
    
    STATE_INDESIGN = 1
    STATE_ENABLED = 2
    STATE_DISABLED = 3
    
    STATES = (
        (STATE_INDESIGN, 'In Design'),
        (STATE_ENABLED, 'Enabled'),
        (STATE_DISABLED, 'Disabled')
    )

    ACCESSIBILITY_USER = 1
    ACCESSIBILITY_NODE = 2
    ACCESSIBILITY_ALL = 3
    
    ACCESSIBILITY = (
        (ACCESSIBILITY_USER, 'Only Myself'),
        (ACCESSIBILITY_NODE, 'Everyone in Node'),
        (ACCESSIBILITY_ALL, 'Everyone')
    )


    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    state = models.PositiveIntegerField(default=1, choices=STATES)
    accessibility = models.PositiveIntegerField(default=ACCESSIBILITY_USER, choices=ACCESSIBILITY)
    apply_sweep_rule = models.BooleanField(default=True)
    version = models.PositiveIntegerField(null=True, blank=True)
    previous_version = models.ForeignKey('RuleGenerator', null=True, blank=True)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    node = models.CharField(max_length=255, null=True)

    @property
    def full_name(self):
        name = self.name
        if self.version:
            name += ' (v. %d)' % self.version
        return name 

    @property
    def state_name(self):
        return dict(RuleGenerator.STATES).get(self.state)

   
    @property
    def is_accessible_by_user(self):
        return self.accessibility == RuleGenerator.ACCESSIBILITY_USER

    @property
    def is_accessible_by_node(self):
        return self.accessibility == RuleGenerator.ACCESSIBILITY_NODE

    @property
    def is_accessible_by_all(self):
        return self.accessibility == RuleGenerator.ACCESSIBILITY_ALL

    @property
    def accessibility_name(self):
        name = dict(RuleGenerator.ACCESSIBILITY).get(self.accessibility)
        if self.is_accessible_by_node:
            name = '%s %s' % (name, str(self.node))
        return name

    @property
    def start_block_rules(self):
        return list(self.rulegeneratorstartblock_set.all())

    @property
    def sample_block_rules(self):
        return list(self.rulegeneratorsampleblock_set.all())

    @property
    def end_block_rules(self):
        return list(self.rulegeneratorendblock_set.all())

    def is_accessible_by(self, user):
        mauser = getMadasUser(user.username)
        if mauser.IsAdmin or mauser.IsMastrAdmin or \
           (self.is_accessible_by_user and user.id == self.created_by.id) or \
           (self.is_accessible_by_node and mauser.PrimaryNode == self.node) or \
           (self.is_accessible_by_all):
           return True
        else:
            return False

    def __unicode__(self):
        return self.full_name

class RuleGeneratorStartBlock(models.Model):
    rule_generator = models.ForeignKey(RuleGenerator)
    index = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    component = models.ForeignKey(Component)

class RuleGeneratorSampleBlock(models.Model):
    ORDER_CHOICES = (
        (1, 'random'),
        (2, 'position')
    )
    rule_generator = models.ForeignKey(RuleGenerator)
    index = models.PositiveIntegerField()
    sample_count = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    component = models.ForeignKey(Component)
    order = models.PositiveIntegerField(choices=ORDER_CHOICES)

    @property
    def in_position(self):
        return self.order == 2

    @property
    def in_random_position(self):
        return self.order == 1

    @property
    def order_name(self):
        if self.in_random_position:
            return 'random order'
        else:
            return 'position'
 
class RuleGeneratorEndBlock(models.Model):
    rule_generator = models.ForeignKey(RuleGenerator)
    index = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    component = models.ForeignKey(Component)
 
