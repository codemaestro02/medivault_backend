from guardian.shortcuts import assign_perm, get_perms
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Consent, Patient
from .serializers import PatientSerializer, ConsentSerializer


# Example: Assign permission when consent is granted
def grant_consent(patient, professional, data_scope):
    # Create a Consent record
    Consent.objects.create(
        patient=patient,
        granted_to=professional,
        data_scope=data_scope
    )

    # Assign object-level permission
    assign_perm('view_patient', professional, patient)


# Example: Check permissions before accessing data
def check_access(professional, patient):
    if 'view_patient' in get_perms(professional, patient):
        return True
    return False


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConsentViewSet(viewsets.ModelViewSet):
    queryset = Consent.objects.all()
    serializer_class = ConsentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True, url_path='grant-consent')
    def grant_consent(self, request, pk=None):
        serializer = ConsentSerializer(data=request.data)
        granted_to = request.user
        if serializer.is_valid():
            patient = serializer.validated_data['patient']
            Consent.objects.create(
                granted_to=granted_to,
                data_scope=serializer.validated_data['data_scope'],
                patient=patient,
                expires_at=serializer.validated_data['expires_at'],
                is_active=serializer.validated_data['is_active']
            )
        return Response(serializer.data, status=status.HTTP_200_OK,
                        message=f"Consent has been given to {granted_to.get_full_name()} by {patient.administrative_data.suffix}. {patient.administrative_data.first_name} {patient.administrative_data.last_name}")
