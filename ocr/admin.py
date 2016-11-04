from django.contrib import admin

# Register your models here.

from .models import ScannedCardMaster, ScannedCardDetail

class ScannedCardMasterAdmin(admin.ModelAdmin):
    model = ScannedCardMaster
    list_display = ('id', 'device_type', 'card_front', 'card_back', 'locale', 'imei')

#def scanned_card():

class ScannedCardAdmin(admin.ModelAdmin):
    model = ScannedCardDetail
    list_display = ('scanned_card', 'text', 'predicated_caption', 'accepted_caption')


admin.site.register(ScannedCardDetail, ScannedCardAdmin)
admin.site.register(ScannedCardMaster, ScannedCardMasterAdmin)

