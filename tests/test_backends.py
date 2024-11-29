import pytest

from django_ip_access.backends import IpAccessBackend

pytestmark = pytest.mark.django_db


class TestIpAccessBackend:
    @staticmethod
    def test_get_user_user_exists(user):
        user = IpAccessBackend.get_user(user.id)
        assert user

    @staticmethod
    def test_get_user_without_existing_user(user):
        user = IpAccessBackend.get_user(user.id + 1)
        assert not user

    @staticmethod
    def test_authenticate_with_inactive_user(request_builder, user):
        user.is_active = False
        user = IpAccessBackend.authenticate(request_builder.get(user))

        assert not user

    @staticmethod
    def test_authenticate_with_active_user(request_builder, ip):
        user = IpAccessBackend.authenticate(
            request_builder.get(ip.user), ip=ip.ip
        )

        assert user
