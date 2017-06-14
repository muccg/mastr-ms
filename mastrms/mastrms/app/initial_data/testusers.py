import datetime
from ...users.models import User, Group

def load_data(**kwargs):
    n1, created = Group.objects.get_or_create(name="Example Node")
    n2, created = Group.objects.get_or_create(name="Another Example Node")

    client, created = User.objects.get_or_create(email="client@example.com", defaults=dict(
        first_name="Client",
        last_name="User",
        is_staff=False,
        is_active=True,
        date_joined="2012-02-14 16:08:20",
        last_login="2012-02-15 15:02:41",
        telephoneNumber="09 123456",
        homePhone="09 123465",
        title="Client Position",
        physicalDeliveryOfficeName="Client Office",
        destinationIndicator="Client Department",
        description="Examples",
        postalAddress="123 Example Lane",
        businessCategory="Example Institute",
        registeredAddress="Prof Example",
        carLicense="Australia (WA)",
        passwordResetKey="",
    ))

    if created:
        client.set_password("client")
        client.save()

    staff, created = User.objects.get_or_create(email="staff@example.com", defaults=dict(
        first_name="Staff", last_name="User",
        is_active=True,
        is_staff=True,
        last_login=datetime.date(2015, 1, 1),
        telephoneNumber="09 123456",
        homePhone="09 234651",
        registeredAddress="Prof Staff Example",
        physicalDeliveryOfficeName="Staff Office",
        description="Staff member",
        businessCategory="Staff Institute",
        title="Staff",
        carLicense="Australia (WA)",
        destinationIndicator="Staff Department",
        postalAddress="111 Staff Way"))

    if created:
        staff.set_password("staff")
        staff.save()

    staff.groups.add(*Group.objects.filter(name__in=[
        "Mastr Staff",
        n1.name,
    ]))
