from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class AdministrativeData(models.Model):
    mrn = models.CharField(max_length=20, unique=True)  # Medical Record Number
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_admission_date = models.DateTimeField()
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    relationship_status = models.CharField(max_length=10, choices=[
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
    ], blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
    ])
    suffix = models.CharField(max_length=10, choices=[
        ('MR', 'Mr'),
        ('MRS', 'Mrs'),
        ('MISS', 'MISS'),
    ], blank=True, null=True)
    blood_group_type = models.CharField(max_length=5, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ])
    rhesus_factor = models.CharField(max_length=5, choices=[
        ('+', '+'),
        ('-', '-'),
    ])
    blood_group = models.CharField(max_length=5, editable=False)
    genotype = models.CharField(max_length=5, choices=[
        ('AA', 'AA'),
        ('AC', 'AC'),
        ('AS', 'AS'),
        ('SC', 'SC'),
        ('SS', 'SS'),
    ])
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    emergency_contact = models.JSONField(default=list)

    objects = models.Manager()


class MedicalData(models.Model):
    allergies = models.JSONField(default=list)
    chronic_conditions = models.JSONField(default=list)
    previous_medications = models.JSONField(default=dict)
    medical_history = models.JSONField()
    family_history = models.JSONField(default=dict)
    surgeries = models.JSONField(default=list)

    objects = models.Manager()
