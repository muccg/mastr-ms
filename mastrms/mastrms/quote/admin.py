from mastrms.quote.models import *
from django.contrib import admin
from django.core import urlresolvers
import urllib

class UserOrganisationInline(admin.TabularInline):
    model = UserOrganisation
    extra = 3

class EmailmapAdmin(admin.ModelAdmin):
    list_display = ['emailaddress']
    search_fields = ['emailaddress']

class FormalquoteAdmin(admin.ModelAdmin):
    list_display = ['quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'status', 'downloaded']
    search_fields = ['details', 'fromemail', 'toemail']
    list_filter = ['status']
    date_hierarchy = 'created'

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'abn', 'projects_link']
    search_fields = ['name', 'abn']
    inlines = [UserOrganisationInline]

    def projects_link(self, obj):
        userorgs = obj.userorganisation_set.all()
        userids = [str(x.user.id) for x in userorgs]
        change_url = urlresolvers.reverse('admin:repository_project_changelist')
        return '<a href="%s?client__id__in=%s">Projects</a>' % (change_url, urllib.quote(','.join(userids)))
    projects_link.short_description = 'Projects'
    projects_link.allow_tags = True

class QuotehistoryAdmin(admin.ModelAdmin):
    list_display = ['quoteid', 'authoremailid', 'newnode', 'oldnode', 'comment', 'completed', 'oldcompleted', 'changetimestamp']
    list_filter = ['completed', 'oldcompleted']
    date_hierarchy = 'changetimestamp'

class QuoterquestAdmin(admin.ModelAdmin):
    list_display = ['emailaddressid', 'tonode', 'details', 'requesttime', 'unread', 'completed', 'firstname', 'lastname', 'officephone', 'country', 'attachment']
    list_filter = ['tonode', 'unread', 'completed']
    date_hierarchy = 'requesttime'

admin.site.register(Emailmap, EmailmapAdmin)
admin.site.register(Formalquote, FormalquoteAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Quotehistory, QuotehistoryAdmin)
admin.site.register(Quoterequest, QuoterquestAdmin)
