from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import HealthPersonnel, Administrator
from .serializers import HealthPersonnelLoginSerializer, HealthPersonnelRegisterSerializer, \
    HealthPersonnelUpdatePasswordSerializer, AdministratorLoginSerializer, AdministratorRegisterSerializer, \
    AdminUpdatePasswordSerializer

from .serializers import HealthPersonnelSerializer


class AdministratorRegisterView(APIView):
    serializer_class = AdministratorRegisterSerializer

    def post(self, request):
        serializer = AdministratorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Admin registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdministratorLoginView(APIView):
    serializer_class = AdministratorLoginSerializer

    def post(self, request):
        serializer = AdministratorLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, role="Administrator", email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "message": "Admin authenticated and logged in successfully"
                }, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdministratorUpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminUpdatePasswordSerializer

    def post(self, request):
        serializer = AdminUpdatePasswordSerializer(data=request.data)
        admin = request.user
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_password = serializer.validated_data.get('confirm_password')
            if admin.check_password(old_password):
                if new_password == confirm_password:
                    admin.set_password(new_password)
                    admin.save()
                    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
                return Response({'error': 'New password and confirm password do not match'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)


class HealthPersonnelRegisterView(APIView):
    serializer_class = HealthPersonnelRegisterSerializer

    def post(self, request):
        serializer = HealthPersonnelRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Health Personnel registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthPersonnelLoginView(APIView):
    serializer_class = HealthPersonnelLoginSerializer

    def post(self, request):
        serializer = HealthPersonnelLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, role="HealthPersonnel", email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "message": "HealthPersonnel authenticated and logged in successfully"
                }, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthPersonnelUpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HealthPersonnelUpdatePasswordSerializer

    def post(self, request):
        serializer = HealthPersonnelUpdatePasswordSerializer(data=request.data)
        health_personnel = request.user
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_password = serializer.validated_data.get('confirm_password')
            if health_personnel.check_password(old_password):
                if new_password == confirm_password:
                    health_personnel.set_password(new_password)
                    health_personnel.save()
                    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
                return Response({'error': 'New password and confirm password do not match'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)


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


class HealthPersonnelArchiveRestoreViewSet(ArchiveRestoreListDetailViewSet):
    queryset = HealthPersonnel.objects.all()
    serializer_class = HealthPersonnelSerializer
    permission_classes = [IsAuthenticated]


class HealthPersonnelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = HealthPersonnelSerializer
    queryset = HealthPersonnel.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
