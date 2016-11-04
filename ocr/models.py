from __future__ import unicode_literals
import uuid

from django.db import models

from .constants import CardSide
# Create your models here.


def scanned_card(instance, filename):
    if filename:
        target_dir = 'cards/'
        _, ext = filename.rsplit('.', 1)
        filename = str(uuid.uuid4()) + '.' + ext
        return '/'.join([target_dir, filename])


class ScannedCardMaster(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    card_front = models.ImageField(upload_to=scanned_card, max_length=254, blank=False, db_column='card_front')
    card_back = models.ImageField(upload_to=scanned_card, max_length=254, blank=True, null=True, db_column='card_back')
    device_type = models.CharField(max_length=50, blank=True, null=True, db_column='device_type')
    imei = models.CharField(max_length=25, blank=True, null=True, db_column='imei')
    locale = models.CharField(max_length=10, default='en', db_column='locale')

    def __unicode__(self):
        return self.device_type

    class Meta:
        db_table = "ocr_scannedcard_master"


class ScannedCardDetail(models.Model):
    FieldChoices = ((1, 'FirstName'), (2, 'LastName'), (3, 'Title'), (4, 'Designation'), (5, 'CompanyName'),
                    (6, 'Email'), (7, 'Website'), (8, 'CellNumber'), (9, 'PhoneNumber'), (10, 'FaxNumber'),
                    (11, 'Address'), (0, ''))
    SideChoices = ((CardSide.FRONT, 'Front'), (CardSide.BACK, 'Back'), (CardSide.UNKNOWN, 'Unknown'))
    scanned_card = models.ForeignKey(ScannedCardMaster, db_column='scannedcard_master_id', related_name='scannedcard_master_id')
    text =  models.CharField(max_length=200, db_column='text')
    predicated_caption = models.IntegerField(choices=FieldChoices, default=0, db_column='predicated_caption')
    bounding_cortdinate = models.CharField(max_length=200, blank=True, db_column='bounding_cortdinate')
    accepted_caption = models.IntegerField(choices=FieldChoices, default=0, db_column='accepted_caption')
    card_side =  models.IntegerField(choices=SideChoices, default=CardSide.UNKNOWN, db_column='card_side')

    class Meta:
        db_table = "ocr_scannedcard_details"