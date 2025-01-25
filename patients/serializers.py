import re

from rest_framework import serializers

from records.models import AdministrativeData, MedicalData
from records.serializers import AdministrativeDataSerializer, MedicalDataSerializer
from users.models import HealthPersonnel

from .models import Patient, Consent


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='patient-detail')
    administrative_data = AdministrativeDataSerializer(many=False, read_only=True)
    medical_data = MedicalDataSerializer(many=False, read_only=True)

    class Meta:
        model = Patient
        fields = ['url', 'insurance_info', 'inactive_reason', 'administrative_data', 'medical_data']
        read_only_fields = ['created_at', 'updated_at', 'is_hidden']

    def validate_rfid_id(self, value):
        """Validate RFID ID format"""
        if not re.match('^[A-Fa-f0-9]{24}$', value):
            raise serializers.ValidationError('Invalid RFID ID format')
        return value.upper()

    def validate_mrn(self, value):
        """Validate MRN format"""
        if not re.match('^[A-Za-z0-9]{1,20}$', value):
            raise serializers.ValidationError('Invalid MRN format')
        return value.upper()


class ConsentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='consent-detail')
    patient = serializers.HyperlinkedRelatedField(view_name='patient-detail',
                                                  queryset=Patient.objects.filter(is_hidden=False))
    granted_to = serializers.HyperlinkedRelatedField(view_name='health-personnel-detail',
                                                     queryset=HealthPersonnel.objects.filter(is_hidden=False,
                                                                                             is_on_duty=True))

    class Meta:
        model = Consent
        fields = ['url', 'patient', 'granted_to', 'is_active']
        read_only_fields = ['granted_at', ]
