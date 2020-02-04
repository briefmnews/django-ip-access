import pytest
from faker import Faker
from django_ip_access.models import IpAddress

faker = Faker()
pytestmark = pytest.mark.django_db


class TestIpAddress:
    def test_str(self, ip):
        assert ip.__str__() == ip.ip

    def test_one_user_can_have_multiple_ip_access(self, ip):
        # GIVEN
        user = ip.user

        # WHEN
        second_ip = IpAddress(user=user, ip=faker.ipv4())
        second_ip.save()
        
        # THEN
        assert user.ipaddress_set.all().count() == 2
