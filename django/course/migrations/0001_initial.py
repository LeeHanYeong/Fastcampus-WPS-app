# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('school', 'School과정'), ('camp', 'Camp과정')], max_length=20, verbose_name='과정 분류')),
                ('title', models.CharField(max_length=50, verbose_name='과정 이름')),
                ('number', models.IntegerField(default=0, verbose_name='기수')),
                ('description', models.CharField(max_length=100, verbose_name='간단설명')),
                ('start_date', models.DateField(verbose_name='과정 시작일')),
                ('end_date', models.DateField(verbose_name='과정 종료일')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LectureVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100, verbose_name='강의 제목')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='설명')),
                ('youtube_url', models.CharField(blank=True, max_length=300)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='해당 코스')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]