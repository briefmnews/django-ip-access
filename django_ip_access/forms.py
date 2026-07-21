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
        """
        Cleans and validates the IPs field.
        - Ensures each IP is well-formatted.
        - Removes duplicates.
        - Validates against existing IPs in the database.
        """
        ips = self.cleaned_data.get("ips")

        list_ips = ips.split()

        # Validate formatting and collect unique IPs
        unique_ips = set()
        errors = []
        for ip in list_ips:
            try:
                ipaddress.ip_network(ip)  # Validate IP format
                unique_ips.add(ip)
            except ValueError:
                errors.append(_(f"{ip} is not well-formatted."))

        # Check for existing IPs in the database
        # Django 5+ rejects unsaved instances in related filters.
        existing_ips = IpAddress.objects.filter(
            ip__in=unique_ips
        ).select_related("user")
        if self.instance.pk is not None:
            existing_ips = existing_ips.exclude(edit_ip_address=self.instance)
        for ip_entry in existing_ips:
            errors.append(
                _(f"{ip_entry.ip} already exists for user {ip_entry.user}.")
            )
            unique_ips.discard(ip_entry.ip)

        if errors:
            raise ValidationError(errors)

        return "\n".join(sorted(unique_ips))
