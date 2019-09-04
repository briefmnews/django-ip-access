from django.contrib import admin

from .models import IpAddress


class IpAddressAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_select_related = ("user",)
    list_display = ("ip", "user")
    ordering = ("user__email",)
    search_fields = ("ip", "user__email")


admin.site.register(IpAddress, IpAddressAdmin)
