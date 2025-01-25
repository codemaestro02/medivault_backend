from rest_framework import serializers

from .models import HealthPersonnel, Administrator


class HealthPersonnelRegisterSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='healthpersonnel-detail')

    class Meta:
        model = HealthPersonnel
        fields = ['url', 'role', 'email', 'first_name', 'last_name', 'contact_number', 'emergency_contact',
                  'specialization', 'department']

    def create(self, validated_data):
        """Create a new healthcare personnel"""
        healthpersonnel = HealthPersonnel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            department=validated_data['department'],
        )
        return healthpersonnel


class HealthPersonnelLoginSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='healthpersonnel-detail')
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = HealthPersonnel
        fields = ['url', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class HealthPersonnelUpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = HealthPersonnel
        fields = ['old_password', 'new_password', 'confirm_password']


class HealthPersonnelSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='healthpersonnel-detail')

    class Meta:
        model = HealthPersonnel
        fields = "__all__"


class AdministratorLoginSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='administrator-detail')
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Administrator
        fields = ['url', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class AdministratorRegisterSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='administrator-detail')

    class Meta:
        model = Administrator
        fields = ['url', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        """Create a new administrator"""
        administrator = Administrator.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return administrator


class AdminUpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Administrator
        fields = ['old_password', 'new_password', 'confirm_password']
