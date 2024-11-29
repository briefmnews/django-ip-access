from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from ipware import get_client_ip

IP_ACCESS_CACHE_KEY_PREFIX = getattr(
    settings, "IP_ACCESS_CACHE_KEY_PREFIX", "ip_auth_"
)
IP_ACCESS_CACHE_TTL = getattr(settings, "IP_ACCESS_CACHE_TTL", 60)


class IpAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            return self.get_response(request)

        ip, _ = get_client_ip(request)
        cache_key = f"{IP_ACCESS_CACHE_KEY_PREFIX}_{ip}"

        if not cache.get(cache_key):
            user = authenticate(request, ip=ip)
            cache.set(cache_key, True, IP_ACCESS_CACHE_TTL)

            if user:
                login(
                    request,
                    user,
                    backend="django_ip_access.backends.IpAccessBackend",
                )

        return self.get_response(request)
