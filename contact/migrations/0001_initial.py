# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-02 13:41
from __future__ import unicode_literals

import contact.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('user', '\uad6c\ub9e4\ud68c\uc6d0'), ('seller', '\ud310\ub9e4\ud68c\uc6d0')], default='user', max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('response_message', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=contact.models.download_file_location)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order_num', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
