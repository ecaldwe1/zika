# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-29 00:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_examplefile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examplefile',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='examplefile',
            name='model_name',
        ),
        migrations.RemoveField(
            model_name='examplefile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='examplefile',
            name='output_generate_date',
        ),
        migrations.RemoveField(
            model_name='examplefile',
            name='population',
        ),
    ]