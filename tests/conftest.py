import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from .factories import IpAddressFactory, UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def ip():
    user = UserFactory(email="fake-user@yahoo.fr", is_active=True)
    return IpAddressFactory(user=user)


@pytest.fixture
def request_builder():
    """Create a request object"""
    return RequestBuilder()


class RequestBuilder(object):
    @staticmethod
    def get(path="/", user=None):
        rf = RequestFactory()
        request = rf.get(path)
        request.user = user or AnonymousUser()

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        return request
