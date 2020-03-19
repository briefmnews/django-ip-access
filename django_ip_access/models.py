from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class EditIpAddress(models.Model):
    ips = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Edit Authorized IP address"
        verbose_name_plural = "Edit Authorized IP addresses"

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.ipaddress_set.all().delete()

        super().save(*args, **kwargs)

        ip_addresses_to_create = []
        for ip in self.ips.split():
            ip_addresses_to_create.append(IpAddress(user=self.user, ip=ip, edit_ip_address=self))

        IpAddress.objects.bulk_create(ip_addresses_to_create)


class IpAddress(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edit_ip_address = models.ForeignKey(
        'EditIpAddress',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name = "Authorized IP address"
        verbose_name_plural = "Authorized IP addresses"

    def __str__(self):
        return self.ip
