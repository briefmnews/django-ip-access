import factory
from faker import Faker

from django.contrib.auth import get_user_model

from django_ip_access.models import EditIpAddress, IpAddress

faker = Faker()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: "hubert{0}@delabatte.fr".format(n))
    username = email


class EditIpAddressFactory(factory.DjangoModelFactory):
    class Meta:
        model = EditIpAddress

    user = factory.SubFactory(UserFactory)


class IpAddressFactory(factory.DjangoModelFactory):
    class Meta:
        model = IpAddress

    ip = faker.ipv4()
    edit_ip_address = factory.SubFactory(EditIpAddressFactory)
    user = factory.SubFactory(UserFactory)
