from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import HealthPersonnel

from .models import Patient


@receiver(pre_save, sender=Patient)
def set_blood_group(sender, instance, **kwargs):
    instance.administrative_data.blood_group = f"{instance.administrative_data.blood_group_type}{instance.administrative_data.rhesus_factor}"
    instance.save()


@receiver(pre_save, sender=Patient)
def set_patient_suffix(sender, instance, **kwargs):
    if instance.administrative_data.gender == 'M':
        instance.administrative_data.suffix = 'MR'
    if instance.administrative_data.gender == 'F':
        if instance.administrative_data.relationship_status == 'Single':
            instance.administrative_data.suffix = 'MISS'
        if instance.administrative_data.relationship_status == 'Married' or instance.administrative_data.relationship_status == 'Divorced':
            instance.administrative_data.suffix = 'MRS'


@receiver(pre_save, sender=Patient)
def assign_doctor(sender, instance, **kwargs):
    list_of_available_doctors = HealthPersonnel.objects.filter(role__name__icontains='doctor', is_on_duty=True,
                                                               is_assigned=False)
    if list_of_available_doctors:
        doctor = list_of_available_doctors.first()
        instance.medical_record.doctor_in_charge = doctor
        instance.save()
    else:
        raise ValueError('This doctor is not available at the moment')
