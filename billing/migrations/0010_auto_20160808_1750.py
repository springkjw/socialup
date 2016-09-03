# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0009_auto_20160808_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transaction_status',
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
