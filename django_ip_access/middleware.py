import fnmatch

from django.conf import settings
from django.contrib.auth import authenticate, login
from ipware import get_client_ip

IP_ACCESS_URLS_WHITELIST = getattr(settings, "IP_ACCESS_URLS_WHITELIST", [])


class IpAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            return self.get_response(request)

        # Construct the full URL for matching
        domain = request.get_host().split(":")[0]  # Remove the port if present
        full_url = f"https://{domain}{request.path_info}"

        # Check for matching patterns
        for pattern in IP_ACCESS_URLS_WHITELIST:
            if fnmatch.fnmatch(full_url, pattern) or fnmatch.fnmatch(
                request.path_info, pattern
            ):
                self._authenticate_user(request)
                return self.get_response(request)

        return self.get_response(request)

    @staticmethod
    def _authenticate_user(request):
        ip, _ = get_client_ip(request)
        user = authenticate(request, ip=ip)
        if user:
            login(
                request,
                user,
                backend="django_ip_access.backends.IpAccessBackend",
            )
