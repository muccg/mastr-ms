from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from mastrms.mdatasync_server.rules import ActionType

class NodeClient(models.Model):
    def default_default_data_path():
        return getattr(settings, "REPO_FILES_ROOT", "")

    def default_username():
        return getattr(settings, "CHMOD_USER", "")

    def default_hostname():
        current_site = Site.objects.get(id=settings.SITE_ID)
        return current_site.domain

    organisation_name = models.CharField(max_length=50)
    site_name = models.CharField(max_length=50)
    station_name = models.CharField(max_length=50)
    default_data_path = models.CharField(max_length=255, default=default_default_data_path, help_text="File upload path on the Mastr-MS server")
    username = models.CharField(max_length=255, default=default_username, help_text="Username to use for the rsync command")
    hostname = models.CharField(max_length=255, default=default_hostname, help_text="rsync destination hostname")
    flags = models.CharField(max_length=255, default="--protocol=30 -rzv --chmod=ug=rwX", help_text="Additional options for client to add to rsync command line")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

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
