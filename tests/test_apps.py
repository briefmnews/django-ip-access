import pytest

from django_ip_access.apps import DjangoIpAccessConfig

pytestmark = pytest.mark.django_db


class TestDjangoIpAccessConfig:
    @staticmethod
    def test_apps():
        assert "django_ip_access" in DjangoIpAccessConfig.name
