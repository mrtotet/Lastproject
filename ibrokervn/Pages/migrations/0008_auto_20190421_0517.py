# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-20 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pages', '0007_auto_20190421_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars'),
        ),
    ]
