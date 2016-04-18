# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def reference_data(apps, schema_editor):
    OrganismType = apps.get_model("repository", "OrganismType")
    ExperimentStatus = apps.get_model("repository", "ExperimentStatus")
    UserInvolvementType = apps.get_model("repository", "UserInvolvementType")
    ComponentGroup = apps.get_model("repository", "ComponentGroup")
    Component = apps.get_model("repository", "Component")

    db_alias = schema_editor.connection.alias

    OrganismType.objects.using(db_alias).bulk_create([
        OrganismType(name=t) for t in [
            "Microbial", "Plant", "Animal",
            "Human", "Synthetic", "Other"
        ]])

    ExperimentStatus.objects.using(db_alias).bulk_create([
        ExperimentStatus(name=st, description=st) for st in [
            "New", "In Design", "Designed", "Processing"
        ]])

    UserInvolvementType.objects.using(db_alias).bulk_create([
        UserInvolvementType(name=t) for t in [
            "Principal Investigator", "Involved User", "Client"
        ]])

    ComponentGroup.objects.using(db_alias).bulk_create([
        ComponentGroup(name=cg) for cg in [
            "Sample", "Standard", "Blank"
        ]])

    Component.objects.using(db_alias).bulk_create([
        Component(
            sample_code="Smp",
            component_group=ComponentGroup.objects.get(name="Sample"),
            sample_type="Sample",
            filename_prefix="sample",
        ),
        Component(
            sample_code="Std",
            component_group=ComponentGroup.objects.get(name="Standard"),
            sample_type="Pure Standard",
            filename_prefix="standard",
        ),
        Component(
            sample_code="pbqc",
            component_group=ComponentGroup.objects.get(name="Sample"),
            sample_type="Pooled Biological QC",
            filename_prefix="pbqc",
        ),
        Component(
            sample_code="iqc",
            component_group=ComponentGroup.objects.get(name="Sample"),
            sample_type="Instrument QC",
            filename_prefix="iqc",
        ),
        Component(
            sample_code="RB",
            component_group=ComponentGroup.objects.get(name="Blank"),
            sample_type="Reagent Blank",
            filename_prefix="reagent",
        ),
        Component(
            sample_code="Sweep",
            component_group=ComponentGroup.objects.get(name="Blank"),
            sample_type="Sweep",
            filename_prefix="sweep",
        ),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20160418_2204'),
    ]

    operations = [
        migrations.RunPython(reference_data),
    ]
