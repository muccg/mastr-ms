from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time
from m.models import Organisation, Formalquote

class OrganismType(models.Model):
    """Currently, Microorganism, Plant, Animal or Human"""
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

       
class BiologicalSource(models.Model):
    experiment = models.ForeignKey('Experiment')
    type = models.ForeignKey(OrganismType)
    information = models.TextField(null=True, blank=True)
    ncbi_id = models.PositiveIntegerField(null=True)
    label = models.CharField(max_length=50, null=True, blank=True)

    
class AnimalInfo(models.Model):
    source = models.ForeignKey(BiologicalSource)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'Unknown')
    )
    sex = models.CharField(max_length=2, choices=GENDER_CHOICES, default=u'U')
    age = models.PositiveIntegerField(null=True, blank=True)
    parental_line = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.sex, str(self.age), self.parental_line)


class PlantInfo(models.Model):
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
    notes = models.TextField(null=True)

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

class Organ(models.Model):
    experiment = models.ForeignKey('Experiment')
    name = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

class ExperimentStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    created_on = models.DateField(null=False, default=date.today)
    client = models.ForeignKey(User, null=True)    
    
    def __unicode__(self):
        return self.title + ' (' + self.client.username + ')'

class Experiment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    comment = models.TextField(null=True)
    users = models.ManyToManyField(User, through='UserExperiment', null=True)
    status = models.ForeignKey(ExperimentStatus, null=True)
    created_on = models.DateField(null=False, default=date.today)
    formal_quote = models.ForeignKey(Formalquote, null=True)
    job_number = models.CharField(max_length=30)
    project = models.ForeignKey(Project)
    # ? files
    
    def ensure_dir(self):
        import settings, os
        
        yearpath = settings.REPO_FILES_ROOT + os.sep + 'experiments/' + str(self.created_on.year)
        monthpath = yearpath + '/' + str(self.created_on.month)
        exppath = monthpath + '/' + str(self.id)
        
        if not os.path.exists(exppath):
            os.makedirs(exppath)

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
    attached_pdf = models.TextField(null=True, blank=True)
    experiments = models.ManyToManyField(Experiment, null=True, blank=True)

    def __unicode__(self):
        return self.label

class Treatment(models.Model):
    experiment = models.ForeignKey('Experiment')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name

class SampleTimeline(models.Model):
    experiment = models.ForeignKey('Experiment')
    timeline = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        if self.timeline == None:
            return ""
        return self.timeline

class SampleClass(models.Model):
    class_id = models.CharField(max_length=255)
    experiment = models.ForeignKey(Experiment)
    biological_source = models.ForeignKey(BiologicalSource, null=True)
    treatments = models.ForeignKey(Treatment, null=True)
    timeline = models.ForeignKey(SampleTimeline,null=True)
    organ = models.ForeignKey(Organ, null=True, blank=True)
    enabled = models.BooleanField(default=True)

class Sample(models.Model):
    sample_id = models.CharField(max_length=255)
    sample_class = models.ForeignKey(SampleClass, null=True)
    experiment = models.ForeignKey(Experiment)
    label = models.CharField(max_length=255)
    comment = models.TextField(null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
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
    user = models.ForeignKey(User, null=True)
    sample = models.ForeignKey(Sample)
    
    def __unicode__(self):
        return str(self.LOG_TYPES[self.type][1]) + ': ' + str(self.description)

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
