# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time
from quote.models import Organisation, Formalquote
from mdatasync_server.models import NodeClient
import grp

class SampleNotInClassException(Exception):
    pass

class NotAuthorizedError(StandardError):
    pass

class MadasUser(User):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        User.__init__(self, *args, **kwargs)
        self.ldap_groups = None

    def set_ldap_groups(self, ldap_groups):
        if ldap_groups is None: ldap_groups = tuple()
        self.ldap_groups = ldap_groups
        
    @property
    def is_admin(self):
        assert self.ldap_groups is not None, "Ldap groups not set"
        return ('Administrators' in self.ldap_groups)

    @property
    def is_noderep(self):
        assert self.ldap_groups is not None, "Ldap groups not set"
        return ('Node Reps' in self.ldap_groups)

    @property
    def is_client(self):
        assert self.ldap_groups is not None, "Ldap groups not set"
        return len(self.ldap_groups) == 0

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
    creator = models.ForeignKey(User)
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
    # ? files
  
    def ensure_dir(self):
        ''' This function calculates where the storage area should be for the experiment data.
            It create the directory if it does not exist.
            It returns a tuple in form (abspath, relpath) where 
                abspath is the absolute path
                relpath is the path, relative to the settings.REPO_FILES_ROOT
        '''
        import settings, os, stat
        
        yearpath = os.path.join('experiments', str(self.created_on.year) )
        monthpath = os.path.join(yearpath, str(self.created_on.month) )
        exppath = os.path.join(monthpath, str(self.id) )
       
        abspath = os.path.join(settings.REPO_FILES_ROOT, exppath)

        if not os.path.exists(abspath):
            os.makedirs(abspath)
            os.chmod(abspath, stat.S_IRWXU|stat.S_IRWXG)
        
        import grp
        groupinfo = grp.getgrnam(settings.CHMOD_GROUP)
        gid = groupinfo.gr_gid
        
        os.chown(abspath, os.getuid(), gid)
            
        return (abspath, exppath)


    def __unicode__(self):
        return self.title

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
        import settings, os
        return os.path.join(settings.REPO_FILES_ROOT, 'sops', self.version, filename)

    attached_pdf = models.FileField(upload_to=_filepath, null=True, blank=True)
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
        if self.treatments is not None:
            if self.treatments.abbreviation is not None:
                val = val + self.treatments.abbreviation
        if self.timeline is not None:
            if self.timeline.abbreviation is not None:
                val = val + self.timeline.abbreviation
        if self.organ is not None:
            if self.organ.abbreviation is not None:
                val = val + self.organ.abbreviation
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
            result += "_%s-%s.d" % (run.id, str(self.id))
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
    rule_generator = models.ForeignKey('RunRuleGenerator')
    
    def sortedSamples(self):
        #TODO if method indicates randomisation and blanks, now is when we would do it
        return self.samples.all()
    
    def __unicode__(self):
        return "%s (%s v.%s)" % (self.title, self.method.title, self.method.version)

    def add_samples(self, queryset):
        '''Takes a queryset of samples'''
        assert self.id, 'Run must have an id before samples can be added'
        for s in queryset:
            if s.is_valid_for_run():
                rs, created = RunSample.objects.get_or_create(run=self, sample=s, sequence=self.samples.count())
                
    def remove_samples(self, queryset):
        assert self.id, 'Run must have an id before samples can be added'
        for s in queryset:
            RunSample.objects.filter(run=self, sample=s).delete()

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
        import settings, os, stat
        
        yearpath = os.path.join('runs', str(self.created_on.year) )
        monthpath = os.path.join(yearpath, str(self.created_on.month) )
        runpath = os.path.join(monthpath, str(self.id) )
       
        abspath = os.path.join(settings.REPO_FILES_ROOT, runpath)

        if not os.path.exists(abspath):
            os.makedirs(abspath)
            os.chmod(abspath, stat.S_IRWXU|stat.S_IRWXG)
            
        groupinfo = grp.getgrnam(settings.CHMOD_GROUP)
        gid = groupinfo.gr_gid
        
        os.chown(abspath, os.getuid(), gid)
    
        return (abspath, runpath)
    

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

    @classmethod 
    def create_sweep(self, run):
        return RunSample.objects.create(run=run, component_id=RunSample.SWEEP_ID)

    @classmethod 
    def create(self, run, component):
        return RunSample.objects.create(run=run, component=component)
 
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
            
    def generate_filename(self):
        if self.is_sample():
            return self.sample.run_filename(self.run)
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

class Component(models.Model):
    sample_type = models.CharField(max_length=255)
    sample_code = models.CharField(max_length=255)
    component_group = models.ForeignKey(ComponentGroup)
    filename_prefix = models.CharField(max_length=50)

class RuleGenerator(models.Model):
    STATES = (
        (1, 'In Design'),
        (2, 'Enabled'),
        (3, 'Disabled')
    )

    ACCESSIBILITY = (
        (1, 'Only Myself'),
        (2, 'Everyone in my Node'),
        (3, 'Everyone')
    )

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    state = models.PositiveIntegerField(default=1, choices=STATES)
    accessibility = models.PositiveIntegerField(default=1, choices=ACCESSIBILITY)
    version = models.PositiveIntegerField(null=True, blank=True)
    previous_version = models.ForeignKey('RuleGenerator', null=True, blank=True)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        name = self.name
        if self.version:
            name += ' (v. %d)' % self.version
        return name 

    def __unicode__(self):
        return self.full_name

class RunRuleGenerator(models.Model):
    METHOD_ORDERS = (
        (1, 'resampled vial'),
        (2, 'individual vial')
    )   
    rule_generator = models.ForeignKey(RuleGenerator)
    number_of_methods = models.IntegerField(default=1)
    order_of_methods = models.IntegerField(choices=METHOD_ORDERS, null=True, blank=True)
   
    @property
    def start_block_rules(self):
        return list(self.rule_generator.rulegeneratorstartblock_set.all())

    @property
    def sample_block_rules(self):
        return list(self.rule_generator.rulegeneratorsampleblock_set.all())

    @property
    def end_block_rules(self):
        return list(self.rule_generator.rulegeneratorendblock_set.all())
 
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

class RuleGeneratorEndBlock(models.Model):
    rule_generator = models.ForeignKey(RuleGenerator)
    index = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    component = models.ForeignKey(Component)
 
