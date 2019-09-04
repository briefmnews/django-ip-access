from django.contrib.auth import login, authenticate
from ipware import get_client_ip


class IpAccessMiddleware:
    """Middleware that allows Ip address authentication"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:
            return response

        ip = get_client_ip(request)
        user = authenticate(request, ip=ip)

        if user:
            login(request, user)

        return response
