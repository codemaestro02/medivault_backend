import json

from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

from records.models import AdministrativeData, MedicalData
from users.models import HealthPersonnel


# Create your models here.


class Patient(models.Model):
    """Enhanced patient model with comprehensive medical information"""
    rfid_id = models.CharField(max_length=24, unique=True)
    administrative_data = models.OneToOneField(AdministrativeData, on_delete=models.CASCADE, related_name='patient')
    medical_data = models.OneToOneField(MedicalData, on_delete=models.CASCADE, related_name='patient')
    insurance_info = models.JSONField()
    is_active = models.BooleanField(default=True)
    inactive_reason = CKEditor5Field(config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    objects = models.Manager()

    def admit(self, examination_ward=None, doctor_in_charge=None):
        self.is_active = True
        self.administrative_data.last_admission_date = timezone.now()
        self.administrative_data.save()
        self.medical_records.create(doctor_in_charge=doctor_in_charge, patient=self,
                                    examination_ward=examination_ward)
        self.save()

    # def discharge(self):
    #     self.is_active = False
    #     self.medical_records.last().discharge_date = timezone.now()
    #     self.modical_records.last().is_opened = False
    #     last_record = json.loads(self.medical_records.last().insurance_info)
    #     self.medical_data.medical_history.append(last_record)
    #     self.medical_records.last().save()
    #     self.save()

    def save(self, *args, **kwargs):
        super(Patient, self).save(*args, **kwargs)


class MedicalRecord(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='medical_records')
    doctor_in_charge = models.ForeignKey('users.HealthPersonnel', on_delete=models.PROTECT,
                                         related_name='medical_records')
    symptoms = CKEditor5Field(config_name='extends', null=True, blank=True)
    examination_ward = models.CharField(max_length=100, null=True, blank=True)
    diagnosis = CKEditor5Field(config_name='extends', null=True, blank=True)
    lab_result = CKEditor5Field(config_name='extends', null=True, blank=True)
    prescription = CKEditor5Field(config_name='extends', null=True, blank=True)
    date_diagnosed = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    is_opened = models.BooleanField(default=True)

    objects = models.Manager()


class Consent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    granted_to = models.ForeignKey(HealthPersonnel, on_delete=models.CASCADE)
    data_scope = models.JSONField()  # e.g., {"lab_results": True, "history": False}
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Consent: {self.patient} -> {self.granted_to}"
