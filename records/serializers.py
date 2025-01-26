from rest_framework import serializers

from .models import AdministrativeData, MedicalData


class AdministrativeDataSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='administrative-data-detail')

    class Meta:
        model = AdministrativeData
        fields = "__all__"
        # exclude = ['mrn']


class MedicalDataSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='medical-data-detail')

    class Meta:
        model = MedicalData
        fields = "__all__"
