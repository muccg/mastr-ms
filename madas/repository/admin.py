from madasrepo.repository.models import *
from django.contrib import admin

class OrganismAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'ncbi_id', 'upper_rank_name')
    search_fields = ['name']

class OrganAdmin(admin.ModelAdmin):
    list_display = ('name', 'tissue', 'cell_type', 'subcellular_cell_type')
    search_fields = ['name']

class BiologicalSourceAdmin(admin.ModelAdmin):
    list_display = ('organism', 'experiment')

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'comment')
    search_fields = ['title']

class ExperimentStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('sex', 'age', 'parental_line')

class OriginDetailsAdmin(admin.ModelAdmin):
    list_display = ('source', 'location', 'detailed_location', 'information')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name','source','description','type')

class TreatmentVariationAdmin(admin.ModelAdmin):
    list_display = ('name','treatment')

class GenotypeAdmin(admin.ModelAdmin):
    list_display = ('name','source')

class SampleAdmin(admin.ModelAdmin):
    list_display = ('label','comment', 'sample_class')

class SampleTimelineAdmin(admin.ModelAdmin):
    list_display = ('source','taken_at')

class StandardOperationProcedureAdmin(admin.ModelAdmin):
    list_display = ('category','responsible', 'label', 'area_where_valid', 'comment', 'organisation', 'version', 'defined_by', 'replaces_document', 'content', 'attached_pdf')

class StandardOperationProcedureCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'public')

class OrganismTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
class UserExperimentAdmin(admin.ModelAdmin):
    list_display = ('user', 'experiment', 'type')   

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'institute')  
    
class UserInvolvementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')   

class GenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'development_stage')
    
class GrowthConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'detailed_location')
    
class LampTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
class SampleClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'biological_source', 'organ')
    

admin.site.register(OrganismType, OrganismTypeAdmin)
admin.site.register(Organism, OrganismAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserInvolvementType, UserInvolvementTypeAdmin)
admin.site.register(Organ, OrganAdmin)
admin.site.register(BiologicalSource, BiologicalSourceAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ExperimentStatus, ExperimentStatusAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(OriginDetails, OriginDetailsAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(TreatmentType, TreatmentTypeAdmin)
admin.site.register(TreatmentVariation, TreatmentVariationAdmin)
admin.site.register(Genotype, GenotypeAdmin)
admin.site.register(Sample,SampleAdmin)
admin.site.register(SampleTimeline,SampleTimelineAdmin)
admin.site.register(StandardOperationProcedure,StandardOperationProcedureAdmin)
admin.site.register(StandardOperationProcedureCategory,StandardOperationProcedureCategoryAdmin)
admin.site.register(UserExperiment,UserExperimentAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(GrowthCondition, GrowthConditionAdmin)
admin.site.register(LampType, LampTypeAdmin)
admin.site.register(SampleClass, SampleClassAdmin)
