from django.contrib.auth import login
from ipware import get_client_ip

from .backends import IpAccessBackend


class IpAccessMiddleware:
    """Middleware that allows Ip address authentication"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:
            return response

        ip, is_routable = get_client_ip(request)
        user = IpAccessBackend.authenticate(request, ip=ip)

        if user:
            login(request, user, backend='django_ip_access.backends.IpAccessBackend')

        return response
