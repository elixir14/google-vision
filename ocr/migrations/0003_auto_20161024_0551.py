# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-24 05:51
from __future__ import unicode_literals

from django.db import migrations, models
import ocr.models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0002_auto_20161022_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scannedcardmaster',
            name='card_back',
            field=models.ImageField(blank=True, db_column='card_back', max_length=254, null=True, upload_to=ocr.models.scanned_card),
        ),
        migrations.AlterField(
            model_name='scannedcardmaster',
            name='card_front',
            field=models.ImageField(blank=True, db_column='card_front', max_length=254, null=True, upload_to=ocr.models.scanned_card),
        ),
    ]