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

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_users),
    ]
