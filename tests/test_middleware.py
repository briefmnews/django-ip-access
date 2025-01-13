import pytest

from django_ip_access.middleware import IpAccessMiddleware

from .views import DummyView

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

    def test_anonymous_user_with_existing_ip_address_match_pattern(
        self, user, ip, mocker, request_builder
    ):
        # GIVEN
        mock_get_client_ip = mocker.patch(
            "django_ip_access.middleware.get_client_ip",
            return_value=(ip.ip, False),
        )
        request = request_builder.get(path="/")

        # WHEN
        DummyView.as_view()(request)

        # THEN
        assert request.user.is_authenticated
        mock_get_client_ip.assert_called_once_with(request)

    def test_anonymous_user_with_existing_ip_address_dont_match_pattern(
        self, ip, mocker, request_builder
    ):
        # GIVEN
        request = request_builder.get(path="/dummy/")
        mock_get_client_ip = mocker.patch(
            "django_ip_access.middleware.get_client_ip",
            return_value=(ip.ip, False),
        )

        # WHEN
        DummyView.as_view()(request)

        # THEN
        assert not request.user.is_authenticated
        assert mock_get_client_ip.call_count == 0

    def test_authenticated_user(self, mocker, user, request_builder, ip):
        # GIVEN
        request = request_builder.get(path="/", user=user)
        mock_get_client_ip = mocker.patch(
            "django_ip_access.middleware.get_client_ip",
            return_value=(ip.ip, False),
        )

        # WHEN
        DummyView.as_view()(request)

        # THEN
        assert mock_get_client_ip.call_count == 0
