from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import HealthPersonnelLoginView, HealthPersonnelRegisterView, AdministratorLoginView, \
    AdministratorRegisterView

from .views import HealthPersonnelViewSet, HealthPersonnelArchiveRestoreViewSet

router = DefaultRouter()
router.register(r'healthpersonnel', HealthPersonnelViewSet, basename='healthpersonnel')
router.register(r'healthpersonnel/archive', HealthPersonnelArchiveRestoreViewSet, basename='healthpersonnel-archive')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/personnel/register', AdministratorRegisterView.as_view(), name='personnel-register'),
    path('api/personnel/login/', HealthPersonnelLoginView.as_view(), name='personnel_login'),
    path('api/admin/login/', AdministratorLoginView.as_view(), name='admin_login'),
    path('api/admin/register/', AdministratorRegisterView.as_view(), name='admin_register'),
]
