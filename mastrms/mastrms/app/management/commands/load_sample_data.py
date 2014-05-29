import os.path
import datetime
import logging
from django.contrib.sites.models import Site
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.auth.models import Group

from ....mdatasync_server.models import NodeClient
from ....repository.models import Project, InstrumentMethod, Experiment, ExperimentStatus, Run, RuleGenerator
from ....users.models import User

logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    help = "Creates data for testing purposes."

    def handle(self, *args, **options):
        admin = User.objects.order_by("id").first()
        user, created = User.objects.get_or_create(username="another@example.com",
                                                   email="another@example.com",
                                                   first_name="Another", last_name="User",
                                                   is_active=True, is_superuser=True,
                                                   is_staff=True,
                                                   telephoneNumber="09 123456",
                                                   homePhone="09 234651",
                                                   registeredAddress="Prof Antoher Example",
                                                   physicalDeliveryOfficeName="Another Office",
                                                   description="Another",
                                                   businessCategory="Another Institute",
                                                   title="Another Position",
                                                   carLicense="Australia (WA)",
                                                   destinationIndicator="Another Department",
                                                   postalAddress="123 Anoter Lane")

        nc, created = NodeClient.objects.get_or_create(organisation_name="org", site_name="site", station_name="station")

        rg, created = RuleGenerator.objects.get_or_create(name="Empty Rule Generator", description="Rule generator for testing", state=RuleGenerator.STATE_ENABLED, accessibility=RuleGenerator.ACCESSIBILITY_ALL, version=1, created_by=admin)

        proj, created = Project.objects.get_or_create(title="Test Project", description="This project is for testing Mastr-MS", client=user)
        proj.managers.add(admin)

        ex, created = Experiment.objects.get_or_create(title="Test experiment", description="This experiment was created for test purposes.", comment="This is a comment about the experiment", status=ExperimentStatus.objects.get(name="Designed"), job_number="000", project=proj, instrument_method=InstrumentMethod.objects.first(), sample_preparation_notes="Example sample preparation notes")

        # todo sample source, timeline, treatments

# class Command(NoArgsCommand):
#     help = "Loads example data"

#     def handle(self, **options):
#         load_debug_data()
#         print "Your data is ready"

def load_debug_data():
    s, _ = User.objects.get_or_create(
        username="client@example.com", defaults={
            "email": "client@example.com",
            "is_superuser": False, "is_staff": True,
            "first_name": "Rodney", "last_name": "Lorrimar",
            "dob": datetime.date(1983, 11, 10), "sex": "M",
            "tokenless_login_allowed": True})
    s.first_name = "Client"
    s.last_name = "User"
    s.set_password("client")
    s.save()

    s.groups.add(Group.objects.get(name="Mastr Staff"))
    s.groups.add(Group.objects.get(name="Example Node"))

    Site.objects.get_or_create(name="localhost", domain="localhost")

    m, _ = Spirit.objects.get_or_create(first_name="Wendy", last_name="Lorrimar", defaults={"second_name": "Maree", "maiden_name": "Styles", "dob": datetime.date(1956, 9, 23), "dob_checked": True, "sex": "F"})
    m.save()

    f, _ = Spirit.objects.get_or_create(first_name="Gary", last_name="Lorrimar", defaults={"second_name": "Wilfrid", "dob": datetime.date(1952, 3, 24), "dob_checked": True, "sex": "M"})
    f.save()

    s.mother = m
    s.father = f
    s.save()

    Spirit.objects.get_or_create(first_name="Chris", last_name="Lorrimar", defaults={"sex": "M", "mother": m, "father": f, "dob": datetime.date(1985, 4, 12)})

    gm1, _ = Spirit.objects.get_or_create(first_name="Betty", last_name="Lorrimar", defaults={
        "second_name": "Gwendoline", "maiden_name": "Vernon", "dob": datetime.date(1930, 5, 24),
        "dob_checked": False, "sex": "F"})
    gm1.save()

    gf1, _ = Spirit.objects.get_or_create(first_name="Wilfrid", last_name="Lorrimar", defaults={
        "dob": datetime.date(1922, 1, 1), "dob_checked": False,
        "dod": datetime.date(1972, 1, 1), "dod_checked": False, "sex": "M"})
    gf1.save()

    f.mother = gm1
    f.father = gf1
    f.save()

    Spirit.objects.get_or_create(first_name="Colin", last_name="Lorrimar", defaults={"dob": datetime.date(1954, 1, 1), "dob_checked": False, "sex": "M", "father": gf1, "mother": gm1})
    Spirit.objects.get_or_create(first_name="Ann", last_name="Lorrimar", defaults={"dob": datetime.date(1955, 1, 1), "dob_checked": False, "sex": "F", "father": gf1, "mother": gm1})
    Spirit.objects.get_or_create(first_name="Ian", last_name="Lorrimar", defaults={"dob": datetime.date(1957, 1, 1), "dob_checked": False, "sex": "F", "father": gf1, "mother": gm1})
    Spirit.objects.get_or_create(first_name="Jennifer", last_name="Lorrimar", defaults={"dob": datetime.date(1958, 1, 1), "dob_checked": False, "sex": "F", "father": gf1, "mother": gm1})

    gm2, _ = Spirit.objects.get_or_create(first_name="Margaret", last_name="Styles", defaults={"second_name": "Dorothy", "dob": datetime.date(1930, 1, 1), "dob_checked": False, "sex": "F"})
    gm2.save()
    gf2, _ = Spirit.objects.get_or_create(first_name="Basil", last_name="Styles", defaults={"second_name": "Hargrave", "dob": datetime.date(1921, 1, 1), "dob_checked": False, "dod": datetime.date(2011, 10, 1), "dod_checked": False, "sex": "M"})
    gf2.save()

    m.mother = gm2
    m.father = gf2
    m.save()

    v, _ = Spirit.objects.get_or_create(first_name="Vicky", last_name="Styles", defaults={"mother": gm2, "father": gf2, "dob": datetime.date(1953, 6, 6), "dob_checked": False, "sex": "F"})
    v.save()

    l, _ = Spirit.objects.get_or_create(first_name="Lynley", last_name="Styles", defaults={"mother": gm2, "father": gf2, "dob": datetime.date(1958, 6, 6), "dob_checked": False, "sex": "F"})
    l.save()


    t, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com", "is_superuser": True, "is_staff": True, "first_name": "Another Admin", "last_name": "User", "second_name": "The"})
    t.first_name = "Admin"
    t.last_name = "User"
    t.save()

    fg, _ = FamilyGroup.objects.get_or_create(desc="My Family")
    FamilyMember.objects.get_or_create(spirit=s, family_group=fg, proband=True)
    for m in (s.mother, s.father, gm1, gf1, gm2, gf2):
        FamilyMember.objects.get_or_create(spirit=m, family_group=fg)
    for m in s.siblings:
        FamilyMember.objects.get_or_create(spirit=m, family_group=fg)

    # Add my contact details
    como = Suburb.objects.get(name__iexact="Como", state__abbrev="WA", postcode="6152")
    murdoch = Suburb.objects.get(name__iexact="Murdoch", state__abbrev="WA")
    brentwood = Suburb.objects.get(name__iexact="Brentwood", state__abbrev="WA", postcode="6153")
    home, _ = ContactDetails.objects.get_or_create(address_line1="5/201 Coode St",
                                                   suburb=como, defaults={
                                                       "email": "work@rodney.id.au",
                                                       "mobile": "+61478983994",
                                                   })
    work, _ = ContactDetails.objects.get_or_create(address_line1="Centre for Comparative Genomics",
                                                   suburb=murdoch, defaults={
                                                       "email": "rlorrimar@ccg.murdoch.edu.au",
                                                       "phone_work": "+61893606088",
                                                       "address_line2": "Murdoch University",
                                                       "contact_person": "Rodney Lorrimar",
                                                   })
    ContactType.objects.get_or_create(name="Home", defaults={"order": 1})
    ContactType.objects.get_or_create(name="Work", defaults={"order": 2})
    SpiritAddress.objects.get_or_create(spirit=s, contact=home,
                                        type=ContactType.objects.get(name="Home"))
    SpiritAddress.objects.get_or_create(spirit=s, contact=work,
                                        type=ContactType.objects.get(name="Work"))

    # add doctors
    gp, _ = DoctorType.objects.get_or_create(name="GP", defaults={"order": 1})
    Title.objects.get_or_create(name="Mr", defaults={"order": 2})

    address, _ = ContactDetails.objects.get_or_create(address_line1="Brentwood Village Medical Centre",
                                                      suburb=brentwood,
                                                      defaults={
                                                          "address_line2": "67 Cranford Ave",
                                                          "phone_work": "(08) 9316 8014",
                                                      })
    doc, _ = Doctor.objects.get_or_create(last_name="Sembi", first_name="Jaspol",
                                          defaults={
                                              "type": gp,
                                              "active": True,
                                              "initials": "J S",
                                              "contact": address,
                                              "title": Title.objects.get(name="Mr"),
                                          })
