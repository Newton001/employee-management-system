# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-09-11 06:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Department',
            new_name='Duty',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='department',
            new_name='duty',
        ),
    ]