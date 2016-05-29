import datetime
from django.conf import settings

from ...mdatasync_server.models import NodeClient
from ...repository.models import RuleGenerator, RuleGeneratorSampleBlock, Component
from ...repository.models import SampleTimeline, Treatment, Organ, Investigation
from ...repository.models import Project, Experiment, UserExperiment, UserInvolvementType
from ...repository.models import StandardOperationProcedure, InstrumentMethod
from ...repository.models import ExperimentStatus, SampleClass, Run

from ...users.models import User, Group

deps = ["testusers"]

nodes = [
    ("ABF", [
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

    proj = load_project()

    exp = load_experiment(proj)

    # Brad Rand7 and Brad Rand Test 8 -- image11
    load_runs(exp)

def load_experiment(proj):
    exp = create_experiment(proj)

    # image08
    load_timelines(exp)
    load_treatments(exp)
    # will need a "Rib - Upper" for screenshot
    load_organs(exp)


def load_project():
    attrs = dict(
        title="CCG-BRL-01 Analysis of Tissue Samples",
        description="Tissue sample from 5 diabetic individuals were taken from two different parts of the body and at two different time points. Tissues were taken from all individuals named as A,B,C,D, and E from P1 and P2 and at time T1. All the individuals then went through some exercise regime and samples were taken again at time T2.",
        created_on=datetime.date(2015, 1, 1),
        client=User.objects.filter(email__startswith="client").first(),
    )
    proj, created = Project.objects.get_or_create(title=attrs["title"], defaults=attrs)
    for name, value in attrs.items():
        setattr(proj, name, value)
    proj.save()
    proj.managers.add(User.objects.filter(email__startswith="bpower").first())
    Investigation.objects.get_or_create(project=proj, title="Main investigation")
    return proj

user_experiment = [
    ("admin", "Principal Investigator"),
    ("amcgregor", "Client"),
    ("bpower", "Involved User"),
]

def create_experiment(proj):
    sop = load_sop()
    attrs = dict(
        project=proj,
        title="Polar metabolite profiling of Chow and High Fat fed humans - 40 samples",
        description="Repeat experiment",
        comment="",
        status=ExperimentStatus.objects.get(name="New"),
        created_on=datetime.date(2015, 1, 1),
        formal_quote=None,
        job_number="62222",
        investigation=None,
        instrument_method=InstrumentMethod.objects.filter(title__istartswith="default").first(),
        sample_preparation_notes="",
    )

    exp, created = Experiment.objects.get_or_create(project=proj, defaults=attrs)
    for name, val in attrs.items():
        setattr(exp, name, val)
    exp.save()

    for mail, role in user_experiment:
        UserExperiment.objects.get_or_create(
            experiment=exp,
            user=User.objects.filter(email__istartswith=mail).first(),
            type=UserInvolvementType.objects.get(name=role),
            defaults=dict(
                additional_info="",
            )
        )

    return exp

organs = [
    ("Pancreas", "PP"),
    ("Rib - upper", "RU"),
    ("Peanut", "PN"),
]

def load_organs(exp):
    for name, abbrev in organs:
        Organ.objects.get_or_create(
            experiment=exp,
            name=name,
            abbreviation=abbrev,
        )

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
        email="bpower@ccg.murdoch.edu.au",
        first_name="Brad",
        last_name="Power",
        is_staff=True,
        is_active=True,
        date_joined="2012-02-14 16:08:20",
        last_login="2012-02-15 15:02:41",
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
    brad, created = User.objects.get_or_create(email=attrs["email"], defaults=attrs)
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

    attrs.update(dict(
        email="amcgregor@ccg.murdoch.edu.au",
        first_name="Andrew",
        last_name="McGregor",
    ))
    user, created = User.objects.get_or_create(email=attrs["email"], defaults=attrs)
    for name, val in attrs.items():
        setattr(user, name, val)
    user.save()


def load_sop():
    StandardOperationProcedure.objects.get_or_create(
        label="Standard",
        defaults=dict(comment="Test"),
    )


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

timelines = [
    ("16:40", "LAA"),
    ("14:20", "MIA"),
    ("12:00", "MID"),
]

treatments = [
    ("Iodine", "IOD"),
    ("Bromine", "BRO"),
    ("Saline", "SAL"),
]

def load_timelines(experiment):
    for t, a in timelines:
        SampleTimeline.objects.get_or_create(
            experiment=experiment,
            abbreviation=a,
            timeline=t,
        )

def load_treatments(experiment):
    for name, abbrev in treatments:
        Treatment.objects.get_or_create(
            experiment=experiment,
            abbreviation=abbrev,
            name=name,
            description="",
        )

runs = [
    ("bpower", "Brad Rand 7"),
    ("bpower", "Brad Rand Test 6"),
]

def load_runs(experiment):
    for user, name in runs:
        attrs = dict(
            experiment=experiment,
            title=name,
            method=InstrumentMethod.objects.filter(title__istartswith="default").first(),
            created_on=datetime.date(2015, 1, 1),
            creator=User.objects.filter(email__startswith=user).first(),
            machine=NodeClient.objects.filter(station_name="NMR").first(),
            rule_generator=RuleGenerator.objects.filter(name__istartswith="ABF Standard").first(),
            state=2,
        )
        run, created = Run.objects.get_or_create(
            experiment=attrs["experiment"],
            title=attrs["title"],
            defaults=attrs,
        )
        for name, value in attrs.items():
            setattr(run, name, value)
        run.save()
