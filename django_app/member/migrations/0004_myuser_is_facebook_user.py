# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20161020_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_facebook_user',
            field=models.BooleanField(default=False),
        ),
    ]
