from django.urls import path, include
from rest_framework.routers import DefaultRouter
from website.views import SiteViewSet, UserRecordViewSet

router = DefaultRouter()
router.register(r'sites', SiteViewSet)
router.register(r'records', UserRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
