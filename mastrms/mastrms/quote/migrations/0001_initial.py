# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emailmap',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('emailaddress', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'emailmap',
                'verbose_name': 'email map',
                'verbose_name_plural': 'email maps',
            },
        ),
        migrations.CreateModel(
            name='Formalquote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('details', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fromemail', models.CharField(max_length=100)),
                ('toemail', models.CharField(max_length=100)),
                ('status', models.CharField(default=b'new', max_length=20)),
                ('downloaded', models.BooleanField()),
                ('purchase_order_number', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'formalquote',
                'verbose_name': 'formal quote',
                'verbose_name_plural': 'formal quotes',
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('abn', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'm_organisation',
            },
        ),
        migrations.CreateModel(
            name='Quotehistory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('newnode', models.CharField(max_length=100)),
                ('oldnode', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('completed', models.BooleanField()),
                ('oldcompleted', models.BooleanField()),
                ('changetimestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'quotehistory',
                'verbose_name': 'quote history',
                'verbose_name_plural': 'quote histories',
            },
        ),
        migrations.CreateModel(
            name='Quoterequest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tonode', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('requesttime', models.DateTimeField(auto_now_add=True)),
                ('unread', models.BooleanField(default=True)),
                ('completed', models.BooleanField(default=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('officephone', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=100)),
                ('attachment', models.TextField()),
            ],
            options={
                'db_table': 'quoterequest',
                'verbose_name': 'quote request',
                'verbose_name_plural': 'quote requests',
            },
        ),
        migrations.CreateModel(
            name='UserOrganisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organisation', models.ForeignKey(to='quote.Organisation')),
            ],
            options={
                'db_table': 'm_userorganisation',
            },
        ),
    ]
