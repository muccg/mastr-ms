import datetime
from django.conf import settings

from ...mdatasync_server.models import NodeClient
from ...repository.models import RuleGenerator, RuleGeneratorSampleBlock, Component

from ...users.models import User, Group

nodes = [
    ("CCG", [
        ("Bio21 Institute Node", [
            "GCM5001",
            "GCM5002",
            "LC-TOF",
            "LC-QTOF",
            "NMR",
        ]),
        ("Botany Uni Melbourne", [
            "Batman GC-MS",
            "Robin GC-MS",
            "QTOF",
            "QQQ",
        ]),
    ]),
]

def load_data(**kwargs):
    load_nodeclients()
    load_users()
    load_rulegenerator()

def load_nodeclients():
    for org, sites in nodes:
        for site, stations in sites:
            Group.objects.get_or_create(name=site)
            for station in stations:
                NodeClient.objects.get_or_create(
                    organisation_name=org,
                    site_name=site,
                    station_name=station,
                    defaults=dict(
                        date_created=datetime.date(2015, 1, 1),
                        last_modified=datetime.date(2015, 1, 1),
                    )
                )

def load_users():
    attrs = dict(
        first_name="Brad",
        last_name="Power",
        is_staff=True,
        is_active=True,
        date_joined="2012-02-14 16:08:20",
        last_login="2012-02-15 15:02:41",
        password="sha1$a8a68$18c83f486556e36c747bb6f39f6210e260ca21ce",
        telephoneNumber="09 123456",
        homePhone="09 123465",
        title="Software Developer",
        physicalDeliveryOfficeName="CCG",
        destinationIndicator="Centre for Comparative Genomics",
        description="Examples",
        postalAddress="South Street",
        businessCategory="Murdoch University",
        registeredAddress="",
        carLicense="Australia (WA)",
        passwordResetKey="",
    )
    brad, created = User.objects.get_or_create(email="bpower@ccg.murdoch.edu.au", defaults=attrs)
    for name, val in attrs.items():
        setattr(brad, name, val)
    if created:
        brad.set_password("brad")
    brad.save()

    brad.groups.add(*Group.objects.filter(name__in=[
        "User",
        "Administrators",
        "Mastr Administrators",
        "Project Leaders",
        "Mastr Staff",
        "Node Reps",
        "Bio21 Institute Node",
    ]))

def load_rulegenerator():
    attrs = dict(
        description="Initial version of Rule Generator for ABF",
        apply_sweep_rule=False,
        created_by=User.objects.get(email__startswith="bpower"),
        created_on=datetime.date(2015, 1, 1),
        accessibility=RuleGenerator.ACCESSIBILITY_NODE,
        node="Bio21 Institute Node",
    )
    rg, created = RuleGenerator.objects.get_or_create(
        name="ABF Standard Rule Generator",
        defaults=attrs)
    for name, val in attrs.items():
        setattr(rg, name, val)
    rg.save()

    sb, created = RuleGeneratorSampleBlock.objects.get_or_create(
        rule_generator=rg,
        index=0,
        defaults=dict(
            component=Component.objects.get(sample_type="Pooled Biological QC"),
            sample_count=3,
            count=4,
            order=1,
        ))

    sb, created = RuleGeneratorSampleBlock.objects.get_or_create(
        rule_generator=rg,
        index=1,
        defaults=dict(
            component=Component.objects.get(sample_type="Reagent Blank"),
            sample_count=10,
            count=1,
            order=2,
        ))
