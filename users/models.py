from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django_ckeditor_5.fields import CKEditor5Field

from .role_types import ROLE_TYPES, DEPARTMENTS


# class Role(models.Model):
#     """Enhanced role model with hierarchical permissions"""
#     name = models.CharField(max_length=50, choices=ROLE_TYPES)
#     department = models.ForeignKey('Department', on_delete=models.PROTECT, related_name='roles')
#     is_hidden = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.name
#
#     def __repr__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         self.group, _ = Group.objects.get_or_create(name=self.name)
#         super(Role, self).save(*args, **kwargs)


# class Department(models.Model):
#     """Department model for healthcare personnel"""
#     name = models.CharField(max_length=100)
#     description = CKEditor5Field(config_name='extends')
#     is_hidden = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.name


class HealthPersonnel(AbstractUser):
    """Extended user model with healthcare-specific fields"""
    role = models.CharField(max_length=50, choices=ROLE_TYPES)
    department = models.CharField(max_length=100, choices=DEPARTMENTS)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        related_name='healthpersonnel_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='healthpersonnel_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    employee_id = models.AutoField(primary_key=True)
    contact_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, null=True, unique=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    working_hours = models.JSONField(default=dict)
    is_on_duty = models.BooleanField(default=True)
    is_assigned = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.get_full_name()} - {self.role}"

    @property
    def find_available_doctors(self):
        available_doctors = self.objects.filter(role__name__icontains='doctor', is_on_duty=True,
                                                is_assigned=False)
        if available_doctors:
            return available_doctors
        return None

    def save(self, *args, **kwargs):
        if self.role == 'DIRECTOR':
            self.is_superuser = True
        self.is_staff = True
        abbr = "".join([i[0] for i in self.role.split(' ')]).upper()
        self.username = f"{abbr}_{self.employee_id}"  # Generate unique username based on role and employee ID
        group, _ = Group.objects.get_or_create(name=self.role)
        self.groups.add(group)
        super(HealthPersonnel, self).save(*args, **kwargs)


class Administrator(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        related_name='administrators',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='administrator_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = True
        super(Administrator, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'
        ordering = ['employee_id']
