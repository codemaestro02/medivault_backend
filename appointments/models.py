from django.db import models
from django.conf import settings

from django_ckeditor_5.fields import CKEditor5Field

from patients.models import Patient
from users.models import HealthPersonnel


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    professional = models.ForeignKey(HealthPersonnel, on_delete=models.CASCADE,
                                     limit_choices_to={'role__in': ['DOCTOR', 'NURSE']})
    date_time = models.DateTimeField()
    notes = CKEditor5Field(null=True, blank=True)

    def __str__(self):
        return f"Appointment: {self.patient} with {self.professional} at {self.date_time}"
