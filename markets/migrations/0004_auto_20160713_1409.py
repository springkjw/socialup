# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 14:09
from __future__ import unicode_literals

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_auto_20160712_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_summernote.fields.SummernoteTextField(blank=True, null=True),
        ),
    ]
