from django.contrib.sites.models import Site

def load_data(**kwargs):
    # fixme: use better default
    Site.objects.get_or_create(name="localhost", domain="localhost")
