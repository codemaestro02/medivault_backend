import re

from rest_framework import serializers

from records.models import AdministrativeData, MedicalData
from records.serializers import AdministrativeDataSerializer, MedicalDataSerializer
from users.models import HealthPersonnel

from .models import Patient, Consent


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='patient-detail')
    administrative_data = AdministrativeDataSerializer(many=False)
    medical_data = MedicalDataSerializer(many=False)

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

    def create(self, validated_data):
        """Create a new patient record"""
        administrative_data = validated_data.pop("administrative_data")

        medical_data = validated_data.pop("medical_data")
        medical_data = MedicalData.objects.create(**medical_data)
        patient = Patient.objects.create(medical_data=medical_data, administrative_data=administrative_data,
                                         **validated_data)
        # MedicalData.objects.create(patient=patient, **medical_data)
        # AdministrativeData.objects.create(patient=patient, mrn=f"PAT{patient.rfid_id}", **administrative_data)
        return patient


class ConsentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='consent-detail')
    patient = serializers.HyperlinkedRelatedField(view_name='patient-detail',
                                                  queryset=Patient.objects.filter(is_hidden=False))
    granted_to = serializers.HyperlinkedRelatedField(view_name='health-personnel-detail',
                                                     queryset=HealthPersonnel.objects.filter(is_active=True,
                                                                                             is_on_duty=True))

    class Meta:
        model = Consent
        fields = ['url', 'patient', 'granted_to', 'is_active']
        read_only_fields = ['granted_at', ]
