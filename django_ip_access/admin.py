from django import forms
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from functools import update_wrapper

from .models import IpAddress

User = get_user_model()


class IpAddressForm(forms.Form):
    list_ips = forms.CharField(
        widget=forms.Textarea,
        required=True,
        help_text="Copy/past ip addresses (one by row)",
    )
    user = forms.EmailField(required=True)

    def clean_user(self):
        user_email = self.cleaned_data.get("user").lower().strip()
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                _(f"User {user_email} does not exist. Please create the user first.")
            )

        return user

    def clean_list_ips(self):
        return self._get_list_ips(self.cleaned_data.get("list_ips"))

    @staticmethod
    def _get_list_ips(list_ips):
        ips = []

        for ip in list_ips.split():
            try:
                validate_ipv4_address(ip)
            except IndexError:
                raise ValidationError(_("ip is madatory"))
            except ValidationError:
                raise ValidationError(_(f"{ip} is not well-formatted."))

            ips.append(ip)

        return ips


class BulkAddIpAddressesView(FormView):
    form_class = IpAddressForm
    template_name = "django_ip_access/admin/bulk_add.html"
    success_url = "admin:django_ip_access_ipaddress_changelist"

    def form_valid(self, form):
        list_ips = form.cleaned_data["list_ips"]
        user = form.cleaned_data["user"]

        for ip in list_ips:
            try:
                IpAddress.objects.create(user=user, ip=ip)
            except IntegrityError:
                messages.warning(
                    self.request, f"{ip} was not created because it already exists."
                )

        messages.info(self.request, "Bulk add finished successfully.")

        return redirect(reverse("admin:django_ip_access_ipaddress_changelist"))


class IpAddressAdmin(admin.ModelAdmin):
    change_list_template = "django_ip_access/admin/change_list.html"

    raw_id_fields = ("user",)
    list_select_related = ("user",)
    list_display = ("ip", "user")
    ordering = ("user__email",)
    search_fields = ("ip", "user__email")

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = super().get_urls()
        urlpatterns.insert(
            0,
            path(
                "bulk/",
                wrap(BulkAddIpAddressesView.as_view()),
                name="%s_%s_bulk" % info,
            ),
        )

        return urlpatterns


admin.site.register(IpAddress, IpAddressAdmin)
