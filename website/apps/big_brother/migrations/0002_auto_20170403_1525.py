# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('big_brother', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagevisit',
            name='post_content',
            field=models.TextField(default=''),
        ),
    ]
