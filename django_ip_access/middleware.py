from django.contrib.auth import login, authenticate
from ipware import get_client_ip


class IpAccessMiddleware:
    """Middleware that allows Ip address authentication"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            return self.get_response(request)

        ip, is_routable = get_client_ip(request)
        user = authenticate(request, ip=ip)

        if user:
            login(request, user, backend="django_ip_access.backends.IpAccessBackend")

        return self.get_response(request)
