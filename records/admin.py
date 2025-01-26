from django.contrib import admin

from .models import AdministrativeData, MedicalData
# Register your models here.
admin.site.register(AdministrativeData)
admin.site.register(MedicalData)