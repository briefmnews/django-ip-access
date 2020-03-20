import pytest
from faker import Faker
from django_ip_access.models import IpAddress, EditIpAddress

faker = Faker()
pytestmark = pytest.mark.django_db


class TestEditIpAddress:
    def test_str(self, edit_ip):
        assert edit_ip.__str__() == str(edit_ip.user)


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
