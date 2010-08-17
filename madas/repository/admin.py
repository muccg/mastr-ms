from madas.admin.ext import ExtJsonInterface
from madas.repository.models import *
from m.models import Organisation, Formalquote
from mdatasync_server.models import NodeClient
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.webhelpers import url
from django.core import urlresolvers
from django.db.models import Q

##
## Most of the Admin classes here override queryset to restrict access, ie row level permissions.
## They also override get_form where necessary to restrict select widgets based on permissions.
##

class RunSampleInline(admin.TabularInline):
    model = RunSample
    extra = 3
    raw_id_fields = ['sample', 'run']

class OrganAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('name', 'detail')
    search_fields = ['name']

    def queryset(self, request):
        qs = super(OrganAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(OrganAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['experiment'].queryset = Experiment.objects.filter(users=request.user)
        return form

class BiologicalSourceAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('type',)

    def queryset(self, request):
        qs = super(BiologicalSourceAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(BiologicalSourceAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['experiment'].queryset = Experiment.objects.filter(users=request.user)
        return form


class ProjectAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('title', 'description', 'created_on', 'client', 'experiments_link')
    search_fields = ['title']
    list_filter = ['client']

    def queryset(self, request):
        qs = super(ProjectAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(experiment__users=request.user)|Q(client=request.user)).distinct()

    def experiments_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_experiment_changelist')
        return '<a href="%s?project__id__exact=%s">Experiments</a>' % (change_url, obj.id)
    experiments_link.short_description = 'Experiments'
    experiments_link.allow_tags = True


class ExperimentAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['title', 'description', 'comment', 'status', 'created_on', 'formal_quote', 'job_number', 'project', 'instrument_method', 'samples_link']
    search_fields = ['title', 'job_number']

    def save_model(self, request, obj, form, change):
        obj.save()
        involvement = UserInvolvementType.objects.get(name="Principal Investigator")
        user_exp, created = UserExperiment.objects.get_or_create(user=request.user, experiment=obj, type=involvement)        
        user_exp.save()

    def queryset(self, request):
        qs = super(ExperimentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(users__id=request.user.id)

    def get_form(self, request, obj=None):
        form = super(ExperimentAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['project'].queryset = Project.objects.filter(managers=request.user)
        return form

    def samples_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_sample_changelist')
        return '<a href="%s?experiment__id__exact=%s">Samples</a>' % (change_url, obj.id)
    samples_link.short_description = 'Samples'
    samples_link.allow_tags = True


class ExperimentStatusAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']

class AnimalInfoAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('sex', 'age', 'parental_line')

    def queryset(self, request):
        qs = super(AnimalInfoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(source__experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(AnimalInfoAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['source'].queryset = BiologicalSource.objects.filter(experiment__users=request.user)
        return form

class TreatmentAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('name','description')

    def queryset(self, request):
        qs = super(TreatmentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(TreatmentAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['experiment'].queryset = Experiment.objects.filter(users=request.user)
        return form

class SampleAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['label', 'comment', 'weight', 'sample_class', 'experiments_link', 'runs_link', 'logs_link', 'sample_class_sequence']
    search_fields = ['label', 'experiment__title', 'sample_class__organ__name']
    actions = ['create_run']
    inlines = [RunSampleInline]

    def queryset(self, request):
        qs = super(SampleAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(SampleAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['sample_class'].queryset = SampleClass.objects.filter(experiment__users=request.user)
        form.base_fields['experiment'].queryset = Experiment.objects.filter(users=request.user)        
        return form

    
    def create_run(self, request, queryset):

        # check that each sample is valid
        samples_valid = True
        message = ''
        for s in queryset:
            if not s.is_valid_for_run():
                samples_valid = False
                message = "Run NOT created as sample (%s, %s) does not have sample class or its class is not enabled." % (s.label, s.experiment)
                break

        if not samples_valid:
            self.message_user(request, message)
        else:
            im, created = InstrumentMethod.objects.get_or_create(title="Default Method", creator=request.user)
            r = Run(method=im, creator=request.user, title="New Run")
            r.save() # need id before we can add many-to-many
            r.add_samples(queryset)
            change_url = urlresolvers.reverse('admin:repository_run_change', args=(r.id,))
            return HttpResponseRedirect(change_url)

    create_run.short_description = "Create Run from samples."

    def experiments_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_experiment_changelist')
        return '<a href="%s?id__exact=%s">%s</a>' % (change_url, obj.experiment.id, obj.experiment.title)
    experiments_link.short_description = 'Experiment'
    experiments_link.allow_tags = True

    def runs_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_run_changelist')
        run_ids = ','.join([str(x.id) for x in obj.run_set.all()])
        return '<a href="%s?id__in=%s">Runs</a>' % (change_url, run_ids)
    runs_link.short_description = 'Runs'
    runs_link.allow_tags = True

    def logs_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_samplelog_changelist')
        return '<a href="%s?sample__id__exact=%s">Logs</a>' % (change_url, obj.id)
    logs_link.short_description = 'Logs'
    logs_link.allow_tags = True    


class SampleTimelineAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('id', 'timeline')

    def queryset(self, request):
        qs = super(SampleTimelineAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(SampleTimelineAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['experiment'].queryset = Experiment.objects.filter(users=request.user)
        return form

    
class InstrumentMethodAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['title', 'method_path', 'method_name', 'version', 'creator', 'created_on', 'randomisation', 'blank_at_start',
                    'blank_at_end', 'blank_position', 'obsolete', 'obsolescence_date', 'run_link']

    def run_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_run_changelist')
        return '<a href="%s?method__id__exact=%s">Runs</a>' % (change_url, obj.id)
    run_link.short_description = 'Runs'
    run_link.allow_tags = True


class StandardOperationProcedureAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('responsible', 'label', 'area_where_valid', 'comment', 'organisation', 'version', 'defined_by', 'replaces_document', 'content', 'attached_pdf')

    def get_form(self, request, obj=None):
        form = super(StandardOperationProcedureAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['experiments'].queryset = Experiment.objects.filter(users=request.user)
        return form


class OrganismTypeAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('id', 'name')
    

class UserExperimentAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('user', 'experiment', 'type')   

    def queryset(self, request):
        qs = super(UserExperimentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(UserExperimentAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['experiment'].queryset = Experiment.objects.filter(users=request.user)
        return form
    

class UserInvolvementTypeAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('id', 'name')   


class PlantInfoAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('id', 'development_stage')

    def queryset(self, request):
        qs = super(PlantInfoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(source__experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(PlantInfoAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['source'].queryset = BiologicalSource.objects.filter(experiment__users=request.user)
        return form
    

class SampleClassAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['id', 'experiment', 'biological_source', 'treatments', 'timeline', 'organ', 'enabled']
    search_fields = ['experiment__title']

    def queryset(self, request):
        qs = super(SampleClassAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(SampleClassAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['experiment'].queryset = Experiment.objects.filter(users=request.user)
        form.base_fields['biological_source'].queryset = BiologicalSource.objects.filter(experiment__users=request.user)
        form.base_fields['treatments'].queryset = Treatment.objects.filter(experiment__users=request.user)
        form.base_fields['timeline'].queryset = SampleTimeline.objects.filter(experiment__users=request.user)
        form.base_fields['organ'].queryset = Organ.objects.filter(experiment__users=request.user)        
        return form


class SampleLogAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['type', 'description', 'user', 'sample']
    search_fields = ['description']

    def queryset(self, request):
        qs = super(SampleLogAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sample__experiment__users=request.user)

    def get_form(self, request, obj=None):
        form = super(SampleLogAdmin, self).get_form(request, obj)
        if request.user.is_superuser:
            return form
        form.base_fields['sample'].queryset = Sample.objects.filter(experiment__users=request.user)
        return form

class RunAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['title', 'method', 'creator', 'created_on', 'output_link', 'experiments_link', 'samples_link']
    search_fields = ['title', 'method__title', 'creator__username', 'creator__first_name', 'creator__last_name']
    inlines = [RunSampleInline]

    def queryset(self, request):
        qs = super(RunAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(samples__experiment__users=request.user) | Q(creator=request.user)).distinct()

    def output_link(self, obj):
        output_url = urlresolvers.reverse('generate_worklist', kwargs={'run_id': obj.id})
        return '<a href="%s">Output</a>' % output_url
    output_link.short_description = 'Output'
    output_link.allow_tags = True    

    def experiments_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_experiment_changelist')
        exp_ids = ','.join([str(x.experiment.id) for x in obj.samples.all()])
        return '<a href="%s?id__in=%s">Experiments</a>' % (change_url, exp_ids)
    experiments_link.short_description = 'Experiments'
    experiments_link.allow_tags = True

    def samples_link(self, obj):
        change_url = urlresolvers.reverse('admin:repository_sample_changelist')
        sample_ids = ','.join([str(x.id) for x in obj.samples.all()])
        return '<a href="%s?id__in=%s">Samples</a>' % (change_url, sample_ids)
    samples_link.short_description = 'Samples'
    samples_link.allow_tags = True


class ClientFileAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['experiment', 'filepath', 'sharetimestamp', 'sharedby', 'downloaded']

    def queryset(self, request):
        qs = super(ClientFileAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(experiment__users=request.user).distinct()
        
class InstrumentSOPAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ['title','enabled']

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
admin.site.register(Run, RunAdmin)
admin.site.register(ClientFile, ClientFileAdmin)
admin.site.register(InstrumentSOP, InstrumentSOPAdmin)