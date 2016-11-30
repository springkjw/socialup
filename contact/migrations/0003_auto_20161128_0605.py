# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-28 06:05
from __future__ import unicode_literals

import contact.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20161127_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=contact.models.download_file_location),
        ),
        migrations.AddField(
            model_name='contact',
            name='user_type',
            field=models.CharField(choices=[('user', '\uad6c\ub9e4\ud68c\uc6d0'), ('seller', '\ud310\ub9e4\ud68c\uc6d0')], default='user', max_length=50),
        ),
    ]