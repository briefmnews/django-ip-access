from django.contrib import admin, messages

from .forms import EditIpAddressForm
from .models import EditIpAddress


class EditIpAddressAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_select_related = ("user",)
    list_display = ("ips", "user")
    ordering = ("user__email",)
    search_fields = ("ips", "user__email")

    form = EditIpAddressForm


admin.site.register(EditIpAddress, EditIpAddressAdmin)
