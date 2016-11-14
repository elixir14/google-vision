from __future__ import unicode_literals
import uuid

from django.db import models

from .constants import CardSide, UserField
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
    FieldChoices = ((UserField.FIRSTNAME, 'FirstName'), (UserField.LASTNAME, 'LastName'),
                    (UserField.TITLE, 'Title'), (UserField.DESIGNATION, 'Designation'),
                    (UserField.COMPANY, 'Company'), (UserField.EMAIL_1, 'Email 1'),
                    (UserField.EMAIL_2, 'Email 2'), (UserField.EMAIL_3, 'Email 3'),
                    (UserField.WEBSITE_1, 'Website 1'), (UserField.WEBSITE_2, 'Website 2'),
                    (UserField.WEBSITE_3, 'Website 3'), (UserField.ADDRESS_1, 'Address 1'),
                    (UserField.ADDRESS_2, 'Address 2'), (UserField.LINKEDIN_PROFILE, 'LinkedIn Profile'),
                    (UserField.PHONE_1, 'Phone 1'), (UserField.PHONE_2, 'Phone 2'),
                    (UserField.PHONE_3, 'Phone 3'),
                    )
    SideChoices = ((CardSide.FRONT, 'Front'), (CardSide.BACK, 'Back'), (CardSide.UNKNOWN, 'Unknown'))
    scanned_card = models.ForeignKey(ScannedCardMaster, db_column='scannedcard_master_id', related_name='scannedcard_master_id')
    text =  models.CharField(max_length=200, db_column='text')
    predicated_caption = models.IntegerField(choices=FieldChoices, default=UserField.UNKNOWN,
                                             db_column='predicated_caption')
    bounding_cortdinate = models.CharField(max_length=200, blank=True, db_column='bounding_cortdinate')
    accepted_caption = models.IntegerField(choices=FieldChoices, default=UserField.UNKNOWN,
                                           db_column='accepted_caption')
    card_side =  models.IntegerField(choices=SideChoices, default=CardSide.UNKNOWN, db_column='card_side')

    class Meta:
        db_table = "ocr_scannedcard_details"