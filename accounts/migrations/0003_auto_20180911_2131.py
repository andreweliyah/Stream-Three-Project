# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-11 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180904_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sub_end',
            field=models.IntegerField(null=True),
        ),
    ]