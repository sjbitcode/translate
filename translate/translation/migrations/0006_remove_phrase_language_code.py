# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 06:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0005_populate_phrase_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phrase',
            name='language_code',
        ),
    ]
