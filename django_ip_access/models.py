from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class IpAddress(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Authorized IP address"
        verbose_name_plural = "Authorized IP addresses"

    def __str__(self):
        return self.ip
