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
        """Check if sales_contact is provided"""
        User = get_user_model()
        sales_email = self.context["request"].POST.get("sales_contact", "[]")
        if sales_email == "":
            error_message = "Sales contact email is required"
            raise serializers.ValidationError(error_message)

        """Check if sales_contact is a sales user"""
        try:
            sales_contact = User.objects.get(email=sales_email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Sales contact email unknown (check typo)"
            )

        if sales_contact.user_type != "SLS":
            error_message = "'Sales email' should be a sales user"
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

    def validate(self, attrs):
        """Check current user is sales contact of client"""
        current_user = self.context.get("request", None).user
        client_email = self.context["request"].POST.get("client", "[]")
        try:
            client_obj = Client.objects.get(email=client_email)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Client email unknown (check typo)")

        clients = Client.objects.filter(sales_contact=current_user)

        if client_obj not in clients:
            raise serializers.ValidationError(
                "Cannot create contract for this client. (Wrong sales user)"
            )
        return super().validate(attrs)

    def create(self, validated_data):
        client_email = self.context["request"].POST.get("client", "[]")
        client_obj = get_object_or_404(Client, email=client_email)
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

    def validate(self, attrs):
        """Check current user is sales contact of client"""
        current_user = self.context.get("request", None).user
        client_email = self.context["request"].POST.get("client", "[]")
        try:
            client_obj = Client.objects.get(email=client_email)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Client email unknown (check typo)")
        clients = Client.objects.filter(sales_contact=current_user)

        if client_obj not in clients:
            raise serializers.ValidationError(
                "Cannot create event for this client. (Wrong sales user)"
            )

        User = get_user_model()
        """Check support contact is filled"""
        support_email = self.context["request"].POST.get("support_contact", "[]")
        if support_email == "":
            raise serializers.ValidationError("'Support contact' email required")

        """Check support contact is a support user"""
        try:
            support_contact_obj = User.objects.get(email=support_email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Support contact email unknown (check typo)"
            )
        if support_contact_obj.user_type != "SPP":
            raise serializers.ValidationError(
                "'Support contact' should by a Support user"
            )
        return super().validate(attrs)

    def create(self, validated_data):
        client_email = self.context["request"].POST.get("client", "[]")
        client_obj = get_object_or_404(Client, email=client_email)

        User = get_user_model()
        support_email = self.context["request"].POST.get("support_contact", "[]")
        support_contact_obj = get_object_or_404(User, email=support_email)

        event = Event.objects.create(
            client=client_obj,
            event_status=validated_data["event_status"],
            support_contact=support_contact_obj,
            attendees=validated_data["attendees"],
            event_date=validated_data["event_date"],
            notes=validated_data["notes"],
        )
        event.save()
        return event
