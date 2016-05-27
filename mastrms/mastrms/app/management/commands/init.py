from django.core.management.base import BaseCommand
from importlib import import_module

from ...initial_data import base
from ...initial_data import sample
from ...initial_data import adminuser
from ...initial_data import testusers
from ...initial_data import screenshots

datasets = ["sample", "adminuser", "testusers", "screenshots"]

class Command(BaseCommand):
    help = """
        Loads initial data for Mastr-MS.

        Possible datasets are:%s
    """ % "".join("\n  - %s" % s for s in datasets)

    def add_arguments(self, parser):
        parser.add_argument('dataset', nargs='*', type=str)

    def handle(self, dataset=[], **options):
        self.stdout.write("Loading Mastr-MS data...")
        base.load_data()
        for name in dataset:
            self.load_module_data(name, **options)
        self.stdout.write("Mastr-MS data is ready.")

    def load_module_data(self, name, **options):
        self.stdout.write("Loading %s..." % name)
        try:
            module = import_module("...initial_data." + name, package=__package__)
        except ImportError:
            self.stderr.write("Unknown dataset \"%s\"" % name)
            return

        for dep in getattr(module, "deps", None) or []:
            self.load_module_data(dep, **options)
        module.load_data(**options)
