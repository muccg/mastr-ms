import os.path
import datetime

from ...mdatasync_server.models import NodeClient
from ...repository.models import Project, InstrumentMethod, Experiment, ExperimentStatus, Run, RuleGenerator
from ...users.models import User, Group

deps = ["testusers"]

def load_data(**kwargs):
    admin = User.objects.order_by("id").first()
    client = User.objects.get(email="client@example.com")

    nc, created = NodeClient.objects.get_or_create(organisation_name="org", site_name="site", station_name="station")

    rg, created = RuleGenerator.objects.get_or_create(name="Empty Rule Generator", description="Rule generator for testing", state=RuleGenerator.STATE_ENABLED, accessibility=RuleGenerator.ACCESSIBILITY_ALL, version=1, created_by=admin)

    proj, created = Project.objects.get_or_create(title="Test Project", description="This project is for testing Mastr-MS", client=client)
    proj.managers.add(admin)

    ex, created = Experiment.objects.get_or_create(title="Test experiment", description="This experiment was created for test purposes.", comment="This is a comment about the experiment", status=ExperimentStatus.objects.get(name="Designed"), job_number="000", project=proj, instrument_method=InstrumentMethod.objects.first(), sample_preparation_notes="Example sample preparation notes")

    # todo sample source, timeline, treatments
