from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time

class OrganismType(models.Model):
    """Currently, Microorganism, Plant, Animal or Human"""
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class Organism(models.Model):
    name = models.CharField(max_length=255)
    rank = models.CharField(max_length=255, null=True)
    ncbi_id = models.PositiveIntegerField(null=True)
    upper_rank_name = models.CharField(max_length=255, null=True)
    type = models.ForeignKey(OrganismType)
    
    def __unicode__(self):
        return self.name
        
class Gender(models.Model):
    """Male or Female"""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class BiologicalSource(models.Model):
    organism = models.ForeignKey(Organism)
    experiment = models.ForeignKey('Experiment')

    def __unicode__(self):
        return self.organism.name
    
class Animal(BiologicalSource):
    sex = models.ForeignKey(Gender, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    parental_line = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.sex.name, str(self.age), self.parental_line)


class Plant(BiologicalSource):
    development_stage = models.CharField(max_length=255, null=True, blank=True)

class Human(BiologicalSource):
    sex = models.ForeignKey(Gender, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)

class Organ(models.Model):
    source = models.ForeignKey(BiologicalSource, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    tissue = models.CharField(max_length=100, null=True, blank=True)
    cell_type = models.CharField(max_length=100, null=True, blank=True)
    subcellular_cell_type = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Genotype(models.Model):
    source = models.ForeignKey(BiologicalSource)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class LocationType(models.Model):
    """Greenhouse or Other"""
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(LocationType)

    def __unicode__(self):
        return self.name

class Origin(models.Model):
    source = models.ForeignKey(BiologicalSource)
    
    def __unicode__(self):
        return 'origin'
    
class OriginDetails(Origin):
    # either location or freetext_location should have a value
    location = models.ForeignKey(Location, null=True)
    detailed_location = models.TextField(null=True)
    information = models.TextField()

    def __unicode__(self):
        return self.detailed_location

class LampType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class GrowthCondition(Origin):
    greenhouse = models.ForeignKey(Location, null=True, blank=True)
    detailed_location = models.TextField(null=True, blank=True)
    growing_place = models.CharField(max_length=255, blank=True)
    seeded_on = models.DateField(null=True, blank=True)
    transplated_on = models.DateField(null=True, blank=True)
    harvested_on = models.DateField(null=True, blank=True)
    harvested_at = models.TimeField(null=True, blank=True)
    night_temp_cels = models.PositiveIntegerField(null=True, blank=True)
    day_temp_cels = models.PositiveIntegerField(null=True, blank=True)
    light_hrs_per_day = models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)
    light_fluence = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    light_source = models.ForeignKey(LampType)
    lamp_details = models.TextField(blank=True)
 
class ExperimentStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    comment = models.TextField(null=True)
    users = models.ManyToManyField(User, through='UserExperiment', null=True)
    status = models.ForeignKey(ExperimentStatus, null=True)
    created_on = models.DateField(null=False, default=date.today)
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

class StandardOperationProcedureCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
class StandardOperationProcedure(models.Model):
    category = models.ForeignKey(StandardOperationProcedureCategory)
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

class TreatmentType(models.Model):
    """Currently, Diet or Other."""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Treatment(models.Model):
    name = models.CharField(max_length=255)
    source = models.ForeignKey(BiologicalSource)
    description = models.TextField(null=True)
    type = models.ForeignKey(TreatmentType, default=1)

    def __unicode__(self):
        return self.name

class TreatmentVariation(models.Model):
    name = models.CharField(max_length=255)
    treatment = models.ForeignKey(Treatment)
    
    def summaryName(self):
        return str(self.treatment.name) + ' (' + str(self.name) + ')'

    def __unicode__(self):
        return self.name

class SampleTimeline(models.Model):
    source = models.ForeignKey(BiologicalSource)
    taken_at = models.TimeField(blank=True, null=True)
    taken_on = models.DateField(default=date.today)
    
    def __unicode__(self):
        if self.taken_at == None:
            return str(self.taken_on)
        else:
            return str(self.taken_on) + ' ' + str(self.taken_at)

class SampleClass(models.Model):
    class_id = models.CharField(max_length=255)
    biological_source = models.ForeignKey(BiologicalSource)
    treatments = models.ForeignKey(TreatmentVariation, null=True)
    timeline = models.ForeignKey(SampleTimeline,null=True)
    origin = models.ForeignKey(Origin, null=True)
    organ = models.ForeignKey(Organ, null=True, blank=True)
    genotype = models.ForeignKey(Genotype, null=True)
    enabled = models.BooleanField(default=True)

class Sample(models.Model):
    sample_id = models.CharField(max_length=255)
    sample_class = models.ForeignKey(SampleClass)
    label = models.CharField(max_length=255)
    comment = models.TextField(null=True)

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

