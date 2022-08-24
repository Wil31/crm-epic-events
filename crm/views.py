from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from .permissions import (
    IsStaff,
    IsSalesOrManagerOrReadOnly,
    IsClientSalesContactOrReadOnly,
    IsContractSalesContactOrReadOnly,
    IsSupportContactOrSalesOrReadOnly,
)


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [
        IsAuthenticated,
        IsStaff,
        IsSalesOrManagerOrReadOnly,
        IsClientSalesContactOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Client.objects.all()

        """Filter request per client last name"""
        last_name = self.request.GET.get("last_name")
        if last_name is not None and last_name != "":
            queryset = queryset.filter(last_name__icontains=last_name)

        """Filter request per client email"""
        email = self.request.GET.get("email")
        if email is not None and email != "":
            queryset = queryset.filter(email__icontains=email)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Client '{instance}' deleted successfully."},
            status=status.HTTP_200_OK,
        )


class ContractViewset(ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [
        IsAuthenticated,
        IsStaff,
        IsSalesOrManagerOrReadOnly,
        IsContractSalesContactOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Contract.objects.all()

        """Filter request per client last name"""
        last_name = self.request.GET.get("last_name")
        if last_name is not None and last_name != "":
            queryset = queryset.filter(client__last_name__icontains=last_name)

        """Filter request per client email"""
        email = self.request.GET.get("email")
        if email is not None and email != "":
            queryset = queryset.filter(client__email__icontains=email)

        """Filter request per contract created date"""
        date_created = self.request.GET.get("date_created")
        if date_created is not None and date_created != "":
            date_obj = datetime.strptime(date_created, "%d/%m/%Y")
            queryset = queryset.filter(date_created__date=date_obj)

        """Filter request per contract amount"""
        amount = self.request.GET.get("amount")
        if amount is not None and amount != "":
            queryset = queryset.filter(amount=amount)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Contract '{instance}' deleted successfully."},
            status=status.HTTP_200_OK,
        )


class EventViewset(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = [
        IsAuthenticated,
        IsStaff,
        IsSupportContactOrSalesOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Event.objects.all()

        """Filter request per client last name"""
        last_name = self.request.GET.get("last_name")
        if last_name is not None and last_name != "":
            queryset = queryset.filter(client__last_name__icontains=last_name)

        """Filter request per client email"""
        email = self.request.GET.get("email")
        if email is not None and email != "":
            queryset = queryset.filter(client__email__icontains=email)

        """Filter request per event date"""
        event_date = self.request.GET.get("event_date")
        if event_date is not None and event_date != "":
            date_obj = datetime.strptime(event_date, "%d/%m/%Y")
            queryset = queryset.filter(event_date__date=date_obj)

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Event '{instance}' deleted successfully."},
            status=status.HTTP_200_OK,
        )
