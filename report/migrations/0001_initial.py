# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-21 10:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import report.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bad_user_description', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('direct_dealing', '\uc9c1\uac70\ub798 \uc720\ub3c4'), ('bad_words', '\uc695\uc124\ube44\ubc29'), ('illegal_promotion', '\ubd88\ubc95 \ud64d\ubcf4 \uc720\ub3c4'), ('etc', '\uae30\ud0c0')], max_length=20)),
                ('detail', models.TextField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=report.models.download_file_location)),
                ('status', models.CharField(choices=[('accept', '\uc2e0\uace0\uc811\uc218'), ('completed', '\ucc98\ub9ac\uc644\ub8cc')], default='accept', max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('bad_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_bad_user', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_writer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
