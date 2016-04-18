# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorganisation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quoterequest',
            name='emailaddressid',
            field=models.ForeignKey(to='quote.Emailmap', db_column=b'emailaddressid'),
        ),
        migrations.AddField(
            model_name='quotehistory',
            name='authoremailid',
            field=models.ForeignKey(to='quote.Emailmap', db_column=b'authoremailid'),
        ),
        migrations.AddField(
            model_name='quotehistory',
            name='quoteid',
            field=models.ForeignKey(to='quote.Quoterequest', db_column=b'quoteid'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='quote.UserOrganisation'),
        ),
        migrations.AddField(
            model_name='formalquote',
            name='quoterequestid',
            field=models.ForeignKey(to='quote.Quoterequest', db_column=b'quoterequestid'),
        ),
    ]
