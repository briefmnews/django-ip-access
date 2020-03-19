from django.contrib import admin, messages

from .forms import EditIpAddressForm
from .models import EditIpAddress, IpAddress


class EditIpAddressAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_select_related = ("user",)
    list_display = ("ips", "user")
    ordering = ("user__email",)
    search_fields = ("ips", "user__email")

    form = EditIpAddressForm


class IpAddressAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_select_related = ("user",)
    list_display = ("ip", "user")
    ordering = ("user__email",)
    search_fields = ("ip", "user__email")
    

admin.site.register(EditIpAddress, EditIpAddressAdmin)
admin.site.register(IpAddress, IpAddressAdmin)
