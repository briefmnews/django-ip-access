import pytest

from django_ip_access.forms import EditIpAddressForm
from django_ip_access.models import IpAddress

pytestmark = pytest.mark.django_db


class TestEditIpAddressForm:
    def test_form_works(self, user):
        # GIVEN
        ips = ["127.0.0.1", "127.0.0.2", "128.0.0.0/24"]
        data = {"ips": "\n".join(ips), "user": user.pk}

        # WHEN
        form = EditIpAddressForm(data=data)

        # THEN
        assert form.is_valid()
        form.save()
        assert IpAddress.objects.all().count() == 256

    def test_form_with_wrong_ip_formatting(self, user):
        # GIVEN
        ips = ["127.0.0.1", "wrong.ip"]
        data = {"ips": "\n".join(ips), "user": user.pk}

        # WHEN
        form = EditIpAddressForm(data=data)

        # THEN
        assert not form.is_valid()
        assert "wrong.ip is not well-formatted." in form.errors["ips"]

    def test_remove_duplicates(self, user):
        # GIVEN
        ips = ["127.0.0.1", "127.0.0.1", "127.0.0.2"]
        data = {"ips": "\n".join(ips), "user": user.pk}

        # WHEN
        form = EditIpAddressForm(data=data)

        # THEN
        assert form.is_valid()
        form.save()
        assert IpAddress.objects.filter(ip__in=ips).count() == 2

    def test_ip_already_exists(self, user, ip):
        """Raise a validation error in case the ip exists for another user"""
        # GIVEN
        ips = [ip.ip]
        data = {"ips": "\n".join(ips), "user": user.pk}

        # WHEN
        form = EditIpAddressForm(data=data)

        # THEN
        assert not form.is_valid()
        assert (
            f"{ip.ip} already exists for user {ip.user}." in form.errors["ips"]
        )
