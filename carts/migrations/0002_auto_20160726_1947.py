# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='line_item_total',
            field=models.IntegerField(default=0),
        ),
    ]
