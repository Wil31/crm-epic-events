from django.contrib import admin

from .models import Client, Contract, Event


class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "sales_contact", "client_status")


class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "status", "amount", "payment_due")


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "event_status",
        "support_contact",
        "attendees",
        "event_date",
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
