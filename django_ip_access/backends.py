from django.contrib.auth import get_user_model

from .models import IpAddress

User = get_user_model()


class IpAccessBackend:
    """Authentication with IP address"""

    @staticmethod
    def authenticate(request, ip=None):
        try:
            ip_address = IpAddress.objects.get(ip=ip, user__is_active=True)
        except IpAddress.DoesNotExist:
            return None

        return ip_address.user

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
