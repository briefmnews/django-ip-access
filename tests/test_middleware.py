import pytest

from django_ip_access.middleware import IpAccessMiddleware

pytestmark = pytest.mark.django_db


class TestIpAccessMiddleware:
    @staticmethod
    def test_init():
        # GIVEN / WHEN
        ip_access_middleware = IpAccessMiddleware("dump response")

        # THEN
        assert ip_access_middleware.get_response == "dump response"

    def test_anonymous_user_without_existing_ip_address(self, request_builder):
        request = request_builder.get
        ip_access_middleware = IpAccessMiddleware(request)

        ip_access_middleware(request())

        assert ip_access_middleware.get_response().path == "/"

    def test_anonymous_user_with_existing_ip_address(self, ip, mocker, request_builder):
        # GIVEN
        request = request_builder.get
        ip_access_middleware = IpAccessMiddleware(request)

        # WHEN
        mocker.patch("django_ip_access.middleware.get_client_ip", return_value=(ip.ip, False))
        ip_access_middleware(request())

        # THEN
        assert ip_access_middleware.get_response().path == "/"

    def test_authenticated_user(self, user, request_builder):
        # GIVEN
        request = request_builder.get
        ip_access_middleware = IpAccessMiddleware(request)

        # WHEN
        ip_access_middleware(request(user=user))

        # THEN
        assert ip_access_middleware.get_response().path == "/"

