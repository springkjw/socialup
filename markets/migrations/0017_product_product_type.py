# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-07 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0016_auto_20161103_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, choices=[('blog', '\ube14\ub85c\uadf8'), ('facebook', '\ud398\uc774\uc2a4\ubd81'), ('instagram', '\uc778\uc2a4\ud0c0\uadf8\ub7a8'), ('kakaostory', '\uce74\uce74\uc624\uc2a4\ud1a0\ub9ac')], max_length=50, null=True),
        ),
    ]