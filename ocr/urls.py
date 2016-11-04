from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from ocr import views

router = DefaultRouter()
# router.register(r'/scannedcard/', views.ScannedCardViewSet, 'ScannedCard')
router.register(r'/acceptedcard/', views.UserAcceptedViewSet, 'UserAccepted')

# urlpatterns = router.urls
urlpatterns = [
    url(r'^scannedcard/', views.scanned_info, name='scanned_info'),
    url(r'^acceptedcard/', views.user_accepted, name='user_accepted'),
    url(r'^accuracy/', views.predictive_accuracy, name='predictive_accuracy')
]