import ipaddress

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class EditIpAddress(models.Model):
    ips = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Edit Authorized IP address"
        verbose_name_plural = "Edit Authorized IP addresses"

    def __str__(self):
        return str(self.user)

    def _generate_ips_list(self):
        ips_list = []
        for ip in self.ips.split():
            try:
                ips_list.append(str(ipaddress.ip_address(ip)))
            except ValueError:
                ips_list += [str(el) for el in ipaddress.ip_network(ip).hosts()]

        return ips_list

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.ipaddress_set.all().delete()

        ips_list = self._generate_ips_list()

        ip_addresses_to_create = []
        for ip in ips_list:
            ip_addresses_to_create.append(
                IpAddress(user=self.user, ip=ip, edit_ip_address=self)
            )

        IpAddress.objects.bulk_create(ip_addresses_to_create)


class IpAddress(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edit_ip_address = models.ForeignKey(
        "EditIpAddress", on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name = "Authorized IP address"
        verbose_name_plural = "Authorized IP addresses"

    def __str__(self):
        return self.ip
