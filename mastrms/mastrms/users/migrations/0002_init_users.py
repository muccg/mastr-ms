# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models

def init_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    Group = apps.get_model("auth", "Group")
    db_alias = schema_editor.connection.alias

    Group.objects.using(db_alias).bulk_create([
        Group(name="User"),
        Group(name="Administrators"),
        Group(name="Mastr Administrators"),
        Group(name="Project Leaders"),
        Group(name="Mastr Staff"),
        Group(name="Node Reps"),
        Group(name="Pending"),
        Group(name="Rejected"),
        Group(name="Deleted"),
        Group(name="Example Node"),
    ])

    u = User.objects.using(db_alias).create(
        email="admin@example.com",
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
    )

    u.groups.add(*Group.objects.using(db_alias).filter(name__in=[
        "User",
        "Administrators",
        "Mastr Administrators",
        "Project Leaders",
        "Mastr Staff",
        "Node Reps",
    ]))


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_users),
    ]
