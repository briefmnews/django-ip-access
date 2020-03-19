# Generated by Django 2.2.11 on 2020-03-20 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_ip_access', '0002_auto_20200204_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditIpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ips', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Edit Authorized IP address',
                'verbose_name_plural': 'Edit Authorized IP addresses',
            },
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='edit_ip_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='django_ip_access.EditIpAddress'),
        ),
    ]
