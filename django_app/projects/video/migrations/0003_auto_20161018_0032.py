# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 00:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20161014_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='video',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 10, 18, 0, 32, 5, 393449, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.Channel'),
        ),
    ]
