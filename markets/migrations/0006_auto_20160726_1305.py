# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 13:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0005_product_refund'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('price', models.IntegerField(default=0)),
                ('sale_price', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='productoption',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.DeleteModel(
            name='ProductOption',
        ),
        migrations.AddField(
            model_name='variation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markets.Product'),
        ),
    ]
