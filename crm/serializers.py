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

    def create(self, validated_data):
        current_user = self.context.get("request", None).user
        client_email = self.context["request"].POST.get("client", "[]")
        client_email_obj = Client.objects.get(email=client_email)
        clients = Client.objects.filter(sales_contact=current_user)

        if client_email_obj not in clients:
            raise serializers.ValidationError(
                "Cannot create contract for this client. (Wrong sales user)"
            )

        contract = Contract.objects.create(
            client=client_email_obj,
            status=validated_data["status"],
            amount=validated_data["amount"],
            payment_due=validated_data["payment_due"],
        )
        contract.save()
        return contract


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
