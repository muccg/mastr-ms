from django.db import models
from datetime import datetime, date, time
from mastrms.mdatasync_server.rules import ActionType

# Create your models here.

class NodeClient(models.Model):
    organisation_name = models.CharField(max_length=50)
    site_name = models.CharField(max_length=50)
    station_name = models.CharField(max_length=50)
    default_data_path = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default="")
    hostname = models.CharField(max_length=255, default="")
    flags = models.CharField(max_length=255, default="")
    date_created = models.DateTimeField(auto_now_add=True) #generate 'now' on INSERT
    last_modified = models.DateTimeField(auto_now = True) #generate 'now' on UPDATE

    def __unicode__(self):
        return "[%s]-[%s]-[%s]" % (self.organisation_name, self.site_name, self.station_name)

NODE_RULE_CHOICES = (
    (ActionType.EXCLUDE, 'EXCLUDE'),
    (ActionType.INCLUDE, 'INCLUDE'),
    (ActionType.UPDATE_EXISTING, 'UPDATE_EXISTING'),
    (ActionType.MOVE, 'MOVE'),
)

class NodeRules(models.Model):
    parent_node = models.ForeignKey(NodeClient)
    rule_category = models.IntegerField(choices = NODE_RULE_CHOICES)
    rule_text = models.TextField()

    class Meta:
        verbose_name = "Node rule"
        verbose_name_plural = "Node rules"

    def __unicode__(self):
        return "%s%s" % (ActionType.CommandLookup[self.rule_category], self.rule_text)
