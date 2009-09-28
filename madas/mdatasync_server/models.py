from django.db import models
from datetime import datetime, date, time
from mdatasync_server.rules import ActionType

# Create your models here.

class NodeClient(models.Model):
    organisation_name = models.CharField(max_length=50)
    site_name = models.CharField(max_length=50)
    station_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True) #generate 'now' on INSERT
    last_modified = models.DateTimeField(auto_now = True) #generate 'now' on UPDATE

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
