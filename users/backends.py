# from django.contrib.auth import get_user_model
from django.apps import apps
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured

from .models import HealthPersonnel, Administrator


def get_admin_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return apps.get_model('users.Administrator', require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed"
            % 'users.Administrator'
        )


def get_personnel_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return apps.get_model('users.HealthPersonnel', require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed"
            % 'users.HealthPersonnel'
        )


class EmailBackend(ModelBackend):
    def admin_authenticate(self, request, email=None, password=None, **kwargs):
        admin_model = get_admin_model()
        try:
            user = admin_model.objects.get(email=email)
        except admin_model.DoesNotExist:
            admin_model().set_password(password)
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def personnel_authenticate(self, request, email=None, password=None, **kwargs):
        personnel_model = get_personnel_model()
        try:
            user = personnel_model.objects.get(email=email)
        except personnel_model.DoesNotExist:
            personnel_model().set_password(password)
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def authenticate(self, request, role, username=None, password=None, email=None, **kwargs):
        if role == "Administrator":
            return self.admin_authenticate(request, email, password, **kwargs)
        if role == "HealthPersonnel":
            return self.personnel_authenticate(request, email, password, **kwargs)
        return None
