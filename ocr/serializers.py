import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from ocr.models import ScannedCardDetail, ScannedCardMaster


class ScannedCardMasterSerializer(serializers.ModelSerializer):

    card_front = serializers.ImageField(max_length=None, use_url=True, required=True)
    card_back = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = ScannedCardMaster
        fields = ('id', 'device_type', 'card_front','card_back', 'locale','imei')
        read_only_fields = ('card_front')


class ScannedCardDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScannedCardDetail
        fields = ('id', 'scanned_card', 'text', 'predicated_caption', 'accepted_caption','card_side')
