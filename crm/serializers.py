from xml.dom import ValidationErr
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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

    def validate(self, data):
        """Check if user_type is sales"""
        user = self.context.get("request", None).user
        if user.user_type != "SLS":
            error_message = f"Only the Sales user can do this action"
            raise serializers.ValidationError(error_message)
        """Check if sales_contact is provided"""
        User = get_user_model()
        sales_email = self.context["request"].POST.get("sales_contact", "[]")
        if sales_email == "":
            error_message = f"Sales contact email is required"
            raise serializers.ValidationError(error_message)
        """Check if sales_contact is a sales user"""
        sales_contact = get_object_or_404(User, email=sales_email)
        if sales_contact.user_type != "SLS":
            error_message = f"'Sales email' should be a sales user"
            raise serializers.ValidationError(error_message)
        return super().validate(data)

    def create(self, validated_data):
        User = get_user_model()
        sales_email = self.context["request"].POST.get("sales_contact", "[]")
        sales_contact = get_object_or_404(User, email=sales_email)
        client = Client.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            mobile=validated_data["mobile"],
            company_name=validated_data["company_name"],
            sales_contact=sales_contact,
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
        client_obj = get_object_or_404(Client, email=client_email)
        clients = Client.objects.filter(sales_contact=current_user)

        if client_obj not in clients:
            raise serializers.ValidationError(
                "Cannot create contract for this client. (Wrong sales user)"
            )

        contract = Contract.objects.create(
            client=client_obj,
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

    def create(self, validated_data):
        current_user = self.context.get("request", None).user
        client_email = self.context["request"].POST.get("client", "[]")
        client_email_obj = Client.objects.get(email=client_email)
        clients = Client.objects.filter(sales_contact=current_user)

        if client_email_obj not in clients:
            raise serializers.ValidationError(
                "Cannot create event for this client. (Wrong sales user)"
            )

        User = get_user_model()
        support_email = self.context["request"].POST.get("support_contact", "[]")
        support_contact_obj = User.objects.get(email=support_email)

        event = Event.objects.create(
            client=client_email_obj,
            event_status=validated_data["event_status"],
            support_contact=support_contact_obj,
            attendees=validated_data["attendees"],
            event_date=validated_data["event_date"],
            notes=validated_data["notes"],
        )
        event.save()
        return event
