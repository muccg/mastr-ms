from urlparse import urlparse
from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
from django.contrib.sites.models import Site


class Command(NoArgsCommand):
    help = 'Sets the django site to the proper configured url'

    def handle(self, *args, **options):
        url = getattr(settings, "SITE_URL", None)
        site_id = getattr(settings, "SITE_ID", None)
        if site_id and url:
            o = urlparse(url)
            if o.netloc:
                Site.objects.filter(id=site_id).update(domain=o.netloc)
            else:
                raise CommandError("Couldn't parse URL \"%s\"" % url)
