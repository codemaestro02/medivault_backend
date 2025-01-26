from django.contrib import admin

# Register your models here.
from .models import Patient, Consent, MedicalRecord
from records.models import AdministrativeData, MedicalData


class ConsentTabularInline(admin.TabularInline):
    model = Consent
    extra = 0
    fields = ['patient', 'granted_to', 'is_active']
    readonly_fields = ['patient', 'granted_to']
    show_change_link = True
    can_delete = False


class MedicalRecordTabularInline(admin.TabularInline):
    model = MedicalRecord
    extra = 0
    fields = ['patient', 'doctor_in_charge', ]
    readonly_fields = ['patient', ]
    show_change_link = True
    can_delete = False


class MedicalDataStackedInline(admin.StackedInline):
    model = MedicalData
    extra = 0
    fields = ['patient', 'blood_type', 'height', 'weight']
    readonly_fields = ['patient']
    show_change_link = True
    can_delete = False


class AdministrativeDataStackedInline(admin.StackedInline):
    model = AdministrativeData
    extra = 0
    fields = ['patient', 'mrn', 'rfid_id', 'insurance_info']
    readonly_fields = ['patient']
    show_change_link = True
    can_delete = False


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['rfid_id', 'is_active']
    list_filter = ['is_active']
    search_fields = ['mrn', 'rfid_id']
    inlines = [ConsentTabularInline,
               MedicalRecordTabularInline]


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'granted_to', 'is_active']
    list_filter = ['is_active']
    search_fields = ['patient', 'granted_to']
    actions = ['grant_consent']
