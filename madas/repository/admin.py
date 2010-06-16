from madas.admin.ext import ExtJsonInterface
from madas.repository.models import *
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.webhelpers import url
from django.core import urlresolvers

class RunSampleInline(admin.TabularInline):
    model = RunSample
    extra = 3
    raw_id_fields = ['sample', 'run']

class OrganAdmin(admin.ModelAdmin):
    list_display = ('name', 'detail')
    search_fields = ['name']

    def queryset(self, request):
        qs = super(OrganAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users__id=request.user.id)


class BiologicalSourceAdmin(admin.ModelAdmin):
    list_display = ('type',)

    def queryset(self, request):
        qs = super(BiologicalSourceAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users__id=request.user.id)


class ProjectAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('title', 'description', 'created_on', 'experiments_link')
    search_fields = ['title']
    list_filter = ['client']

    def queryset(self, request):
        qs = super(ProjectAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users__id=request.user.id)

    def experiments_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_experiment_changelist')
        return '<a href="%s?project__id__exact=%s">Experiments</a>' % (change_url, obj.id)
    experiments_link.short_description = 'Experiments'
    experiments_link.allow_tags = True


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'comment', 'status', 'created_on', 'formal_quote', 'job_number', 'project', 'instrument_method', 'samples_link']
    search_fields = ['title', 'job_number']

    def queryset(self, request):
        qs = super(ExperimentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(users__id=request.user.id)

    def samples_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_sample_changelist')
        return '<a href="%s?experiment__id__exact=%s">Samples</a>' % (change_url, obj.id)
    samples_link.short_description = 'Samples'
    samples_link.allow_tags = True


class ExperimentStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']

class AnimalInfoAdmin(admin.ModelAdmin):
    list_display = ('sex', 'age', 'parental_line')

    def queryset(self, request):
        qs = super(AnimalInfoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(source__experiment__users__id=request.user.id)


class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name','description')

    def queryset(self, request):
        qs = super(TreatmentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users__id=request.user.id)


class SampleAdmin(admin.ModelAdmin):
    list_display = ['label', 'experiment', 'comment', 'weight', 'sample_class', 'logs_link']
    search_fields = ['label', 'experiment__title', 'sample_class__organ__name']
    actions = ['create_run']
    inlines = [RunSampleInline]

    def queryset(self, request):
        qs = super(SampleAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users__id=request.user.id)

    # customise the sample class drop down
    def get_form(self, request, obj=None):
        form = super(SampleAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['sample_class'].queryset = SampleClass.objects.filter(experiment__users__id=request.user.id)
        return form

    
    def create_run(self, request, queryset):

        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

        im, created = InstrumentMethod.objects.get_or_create(title="Default Method", creator=request.user)
        r = Run(method=im, creator=request.user, title="New Run")
        r.save() # need id before we can add many-to-many


        # check that each sample has a sample class
        samples_valid = True
        message = ''
        for sample_id in selected:
            s = Sample.objects.get(id=sample_id)
            if not s.sample_class or s.sample_class.enabled is False:
                samples_valid = False
                message = "Run NOT created as sample (%s, %s) does not have sample class or its class is not enabled." % (s.label, s.experiment)
                break

        if not samples_valid:
            self.message_user(request, message)
        else:
            for sample_id in selected:
                s = Sample.objects.get(id=sample_id)
                rs = RunSample(run=r, sample=s)
                rs.save()

            change_url = urlresolvers.reverse('admin:repository_run_change', args=(r.id,))
            return HttpResponseRedirect(change_url)

    create_run.short_description = "Create Run from samples."

    def logs_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_samplelog_changelist')
        return '<a href="%s?sample__id__exact=%s">Logs</a>' % (change_url, obj.id)
    logs_link.short_description = 'Logs'
    logs_link.allow_tags = True    


class SampleTimelineAdmin(admin.ModelAdmin):
    list_display = ('id', 'timeline')

    def queryset(self, request):
        qs = super(SampleTimelineAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users__id=request.user.id)

    
class InstrumentMethodAdmin(admin.ModelAdmin):
    list_display = ['title', 'method_path', 'method_name', 'version', 'creator', 'created_on', 'randomisation', 'blank_at_start',
                    'blank_at_end', 'blank_position', 'obsolete', 'obsolescence_date', 'run_link']

    def run_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_run_changelist')
        return '<a href="%s?method__id__exact=%s">Runs</a>' % (change_url, obj.id)
    run_link.short_description = 'Runs'
    run_link.allow_tags = True


class StandardOperationProcedureAdmin(admin.ModelAdmin):
    list_display = ('responsible', 'label', 'area_where_valid', 'comment', 'organisation', 'version', 'defined_by', 'replaces_document', 'content', 'attached_pdf')

class OrganismTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
class UserExperimentAdmin(admin.ModelAdmin):
    list_display = ('user', 'experiment', 'type')   

class UserInvolvementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')   

class PlantInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'development_stage')

    def queryset(self, request):
        qs = super(PlantInfoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(source__experiment__users__id=request.user.id)
    
class SampleClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'experiment', 'biological_source', 'treatments', 'timeline', 'organ', 'enabled']
    search_fields = ['experiment__title']

    def queryset(self, request):
        qs = super(SampleClassAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users__id=request.user.id)


class SampleLogAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'user', 'sample']
    search_fields = ['description']

    def queryset(self, request):
        qs = super(SampleLogAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sample__experiment__users__id=request.user.id)

class RunAdmin(admin.ModelAdmin):
    list_display = ['title', 'method', 'creator', 'created_on', 'output_link']
    search_fields = ['title', 'method__title', 'creator__username', 'creator__first_name', 'creator__last_name']
    inlines = [RunSampleInline]

##    def queryset(self, request):
##        qs = super(RunAdmin, self).queryset(request)
##        if request.user.is_superuser:
##            return qs
##        return qs.filter(samples__experiment__users__id=request.user.id).distinct()

    def output_link(self, obj):
        output_url = urlresolvers.reverse('generate_worklist', kwargs={'run_id': obj.id})
        return '<a href="%s">Output</a>' % output_url
    output_link.short_description = 'Output'
    output_link.allow_tags = True    


admin.site.register(OrganismType, OrganismTypeAdmin)
admin.site.register(UserInvolvementType, UserInvolvementTypeAdmin)
admin.site.register(Organ, OrganAdmin)
admin.site.register(BiologicalSource, BiologicalSourceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(InstrumentMethod, InstrumentMethodAdmin)
admin.site.register(ExperimentStatus, ExperimentStatusAdmin)
admin.site.register(AnimalInfo, AnimalInfoAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Sample,SampleAdmin)
admin.site.register(SampleTimeline,SampleTimelineAdmin)
admin.site.register(StandardOperationProcedure,StandardOperationProcedureAdmin)
admin.site.register(UserExperiment,UserExperimentAdmin)
admin.site.register(PlantInfo, PlantInfoAdmin)
admin.site.register(SampleClass, SampleClassAdmin)
admin.site.register(SampleLog, SampleLogAdmin)
admin.site.register(Run)
