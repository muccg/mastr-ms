from ...users.models import User, Group

def load_data(**kwargs):
    u, created = User.objects.get_or_create(email="admin@example.com", defaults=dict(
        first_name="Admin",
        last_name="User",
        is_staff=True,
        is_active=True,
        date_joined="2012-02-14 16:08:20",
        last_login="2012-02-15 15:02:41",
        password="sha1$a8a68$18c83f486556e36c747bb6f39f6210e260ca21ce",
        telephoneNumber="09 123456",
        homePhone="09 123465",
        title="Example Position",
        physicalDeliveryOfficeName="Example Office",
        destinationIndicator="Example Department",
        description="Examples",
        postalAddress="123 Example Lane",
        businessCategory="Example Institute",
        registeredAddress="Prof Example",
        carLicense="Australia (WA)",
        passwordResetKey="",
    ))

    u.groups.add(*Group.objects.filter(name__in=[
        "User",
        "Administrators",
        "Mastr Administrators",
        "Project Leaders",
        "Mastr Staff",
        "Node Reps",
    ]))
