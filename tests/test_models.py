import pytest

pytestmark = pytest.mark.django_db


class TestIpAddress:
    def test_str(self, ip):
        assert ip.__str__() == ip.ip
