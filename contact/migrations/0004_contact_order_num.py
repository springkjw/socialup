# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-28 06:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0014_auto_20161114_1502'),
        ('contact', '0003_auto_20161128_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='order_num',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.Order'),
        ),
    ]