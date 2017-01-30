# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foreign_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModelRenamedApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='TestSecondModelRenamedApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_m2m', models.ManyToManyField(to='foreign_app.TestRenamedModel')),
            ],
        ),
    ]
