# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address', db_index=True)),
                ('first_name', models.CharField(max_length=50, verbose_name=b'first name', blank=True)),
                ('last_name', models.CharField(max_length=50, verbose_name=b'last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('telephoneNumber', models.CharField(max_length=255, blank=True)),
                ('homePhone', models.CharField(max_length=255, blank=True)),
                ('physicalDeliveryOfficeName', models.CharField(max_length=255, blank=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('destinationIndicator', models.CharField(max_length=255, blank=True)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('postalAddress', models.CharField(max_length=255, blank=True)),
                ('businessCategory', models.CharField(max_length=255, blank=True)),
                ('registeredAddress', models.CharField(max_length=255, blank=True)),
                ('carLicense', models.CharField(max_length=255, blank=True)),
                ('passwordResetKey', models.CharField(max_length=255, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
