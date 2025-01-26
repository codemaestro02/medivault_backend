from drf_spectacular.utils import extend_schema, OpenApiParameter
from guardian.shortcuts import assign_perm, get_perms
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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


class PatientViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     GenericViewSet):
    queryset = Patient.objects.filter(is_hidden=False)
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True, url_path='admit')
    def admit(self, request, pk=None):
        patient = self.queryset.get(pk=pk)
        patient.admit()
        return Response({'message': 'Patient admitted'}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, url_path='discharge')
    def discharge(self, request, pk=None):
        patient = self.queryset.get(pk=pk)
        patient.discharge()
        return Response({'message': 'Patient discharged'}, status=status.HTTP_200_OK)

class ArchiveRestoreListDetailViewSet(mixins.DestroyModelMixin, GenericViewSet):

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=pk, is_active=True)
            instance.is_active = False
            instance.save()
            return Response({'message': 'Successfully Archived'}, status=status.HTTP_200_OK)
        except self.queryset.model.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        responses={'200': None},
        description="List all archived instances"
    )
    @action(detail=False, methods=['get'])
    def archived_list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_active=False)
        try:
            if queryset:
                archived_count = queryset.count()
                serializer = self.serializer_class(queryset, many=True)
                return Response(
                    {'archived_count': archived_count, 'message': 'List of Successfully Retrieved Archived Models',
                     'data': serializer.data})
            return Response({'archived_count': 0, 'error': 'No archived models found'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        responses={'200': None},
        parameters=[
            OpenApiParameter(name='employee_id', type=int, location='path', required=True,
                             description="Retrieve by Id"),
        ],
        description="Retrieve a specific archived instance by employee ID."
    )
    @action(detail=True, methods=['get'])
    def archived_retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.queryset.filter(is_active=False)
        queryset = queryset.filter(pk=pk)
        try:
            if queryset:
                serializer = self.serializer_class(queryset.first())
                return Response({'message': 'Successfully Retrieved Archived Models', 'data': serializer.data})
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        responses={'200': None},
        parameters=[
            OpenApiParameter(name='employee_id', type=int, location='path', required=True, description="Restore by Id"),
        ],
        description="Restore a specific instance by employee ID."
    )
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=pk, is_active=False)
            instance.is_active = True
            instance.save()
            return Response({'message': 'Successfully Restored'}, status=status.HTTP_200_OK)
        except self.queryset.model.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PatientArchiveRestoreViewSet(ArchiveRestoreListDetailViewSet):
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
            # patient = serializer.validated_data['patient']
            patient = Patient.objects.get(pk=pk)
            Consent.objects.create(
                granted_to=granted_to,
                data_scope=serializer.validated_data['data_scope'],
                patient=patient,
                expires_at=serializer.validated_data['expires_at'],
                is_active=serializer.validated_data['is_active']
            )
            assign_perm('view_patient', granted_to, patient)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        message=f"Consent has been given to {granted_to.get_full_name()} by {patient.administrative_data.suffix}. {patient.administrative_data.first_name} {patient.administrative_data.last_name}")

    @action(methods=['GET'], detail=True, url_path='check-access')
    def check_access(self, request, pk=None):
        professional = request.user
        patient = Patient.objects.get(pk=pk)
        if check_access(professional, patient):
            return Response({'message': 'Access granted'}, status=status.HTTP_200_OK)
        return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
