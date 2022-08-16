from django.contrib.auth import get_user_model
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

    def create(self, validated_data):
        User = get_user_model()
        sales_email = self.context["request"].POST.get("sales_contact", "[]")
        sales_contact_obj = User.objects.get(email=sales_email)

        client = Client.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            mobile=validated_data["mobile"],
            company_name=validated_data["company_name"],
            sales_contact=sales_contact_obj,
            client_status=validated_data["client_status"],
        )
        client.save()
        return client


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
