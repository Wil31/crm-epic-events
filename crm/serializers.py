from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Client, Contract, Event


class ClientSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(source="sales_contact.email")

    class Meta:
        model = Client
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "mobile",
            "company_name",
            "sales_contact",
            "client_status",
            "date_created",
            "date_updated",
        ]


class ContractSerializer(ModelSerializer):
    client = serializers.ReadOnlyField(source="client.email")

    class Meta:
        model = Contract
        fields = [
            "id",
            "client",
            "status",
            "amount",
            "payment_due",
            "date_created",
            "date_updated",
        ]


class EventSerializer(ModelSerializer):
    client = serializers.ReadOnlyField(source="client.email")
    support_contact = serializers.ReadOnlyField(source="support_contact.email")

    class Meta:
        model = Event
        fields = [
            "id",
            "client",
            "event_status",
            "support_contact",
            "attendees",
            "event_date",
            "notes",
            "date_created",
            "date_updated",
        ]
