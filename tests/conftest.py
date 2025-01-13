import pytest
from django.contrib.auth import BACKEND_SESSION_KEY, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from django_ip_access.middleware import IpAccessMiddleware

from .factories import EditIpAddressFactory, IpAddressFactory, UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def ip(user):
    user = UserFactory()
    return IpAddressFactory(user=user)


@pytest.fixture
def edit_ip():
    user = UserFactory()
    return EditIpAddressFactory(user=user)


def _http_request(request):
    return request


@pytest.fixture
def request_builder():
    """Create a request object"""
    return RequestBuilder()


class RequestBuilder(object):
    @staticmethod
    def get(
        path="/",
        user=None,
        auth_backend="django_ip_access.backends.IpAccessBackend",
    ):
        rf = RequestFactory()
        request = rf.get(path=path)
        if user:
            user.backend = auth_backend
        request.user = user or AnonymousUser()

        middleware = SessionMiddleware("dummy")
        middleware.process_request(request)
        request.session[BACKEND_SESSION_KEY] = auth_backend
        request.session.save()
        if user:
            login(request, user)
        middleware = IpAccessMiddleware(_http_request)
        request = middleware(request)

        return request
