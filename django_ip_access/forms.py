import ipaddress

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import EditIpAddress, IpAddress


class EditIpAddressForm(forms.ModelForm):
    class Meta:
        model = EditIpAddress
        help_texts = {"ips": _("One ip address per row.")}
        fields = "__all__"

    def clean_ips(self):
        return self._get_cleaned_ips()

    def _get_cleaned_ips(self):
        ips = self.cleaned_data.get("ips")

        # Validate ips
        list_ips = []

        for ip in ips.split():
            try:
                ipaddress.ip_network(ip)
            except ValueError:
                raise ValidationError(_(f"{ip} is not well-formatted."))

            list_ips.append(ip)

        # Remove duplicates
        duplicate_ips = set(
            [(ip, list_ips.count(ip)) for ip in list_ips if list_ips.count(ip) > 1]
        )
        for ip, count in duplicate_ips:
            ips = ips.replace(ip, "", count - 1)

        # Remove existing ips from another user
        for ip in ips.split():
            try:
                ip_address = IpAddress.objects.exclude(edit_ip_address=self.instance or None).get(ip=ip)
                raise ValidationError(
                    _(f"{ip_address.ip} already exists for user {ip_address.user}.")
                )
            except IpAddress.DoesNotExist:
                pass

        return ips.strip()
