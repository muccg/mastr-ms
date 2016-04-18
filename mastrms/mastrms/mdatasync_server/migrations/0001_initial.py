# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mastrms.mdatasync_server.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NodeClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organisation_name', models.CharField(max_length=50)),
                ('site_name', models.CharField(max_length=50)),
                ('station_name', models.CharField(max_length=50)),
                ('default_data_path', models.CharField(default=mastrms.mdatasync_server.models.client_default_default_data_path, help_text=b'File upload path on the Mastr-MS server', max_length=255)),
                ('username', models.CharField(default=mastrms.mdatasync_server.models.client_default_username, help_text=b'Username to use for the rsync command', max_length=255)),
                ('hostname', models.CharField(default=mastrms.mdatasync_server.models.client_default_hostname, help_text=b'rsync destination hostname', max_length=255)),
                ('flags', models.CharField(default=b'--protocol=30 -rzv --chmod=ug=rwX', help_text=b'Additional options for client to add to rsync command line', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('samplefile_ext', models.CharField(default=b'.d', help_text=b'File suffix that the instrument software uses for sample files. Include the dot if necessary.', max_length=255, verbose_name=b'Sample file extension', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NodeRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule_category', models.IntegerField(choices=[(1, b'EXCLUDE'), (2, b'INCLUDE'), (4, b'UPDATE_EXISTING'), (8, b'MOVE')])),
                ('rule_text', models.TextField()),
                ('parent_node', models.ForeignKey(to='mdatasync_server.NodeClient')),
            ],
            options={
                'verbose_name': 'Node rule',
                'verbose_name_plural': 'Node rules',
            },
        ),
    ]
