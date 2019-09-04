from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class IpAddress(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip
