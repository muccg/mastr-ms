from mdatasync_server.models import *
from django.contrib import admin
from madas.admin.ext import ExtJsonInterface


class NodeClientAdmin(ExtJsonInterface, admin.ModelAdmin):
    list_display = ('organisation_name', 'site_name', 'station_name', 'date_created', 'last_modified')

class NodeRulesAdmin(admin.ModelAdmin):
    list_display = ('rule_category', 'rule_text')

admin.site.register(NodeClient, NodeClientAdmin)
admin.site.register(NodeRules, NodeRulesAdmin)

