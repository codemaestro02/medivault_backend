from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, ConsentViewSet, PatientArchiveRestoreViewSet

router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')
router.register(r'consents', ConsentViewSet, basename='consent')
router.register(r'archive', PatientArchiveRestoreViewSet, basename='archive')

urlpatterns = [
    path('', include(router.urls)),
]