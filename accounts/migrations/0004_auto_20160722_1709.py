# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_seller_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
