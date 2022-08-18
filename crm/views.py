from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from .permissions import IsSalesContactOrReadOnly, IsSalesOrManagerUser, IsStaff


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsSalesContactOrReadOnly, IsStaff]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.user_type == "MNG":
            queryset = Client.objects.all()
        elif current_user.user_type == "SLS":
            queryset = Client.objects.filter(sales_contact=current_user)
        elif current_user.user_type == "SPP":
            queryset = Client.objects.filter(
                event__support_contact=current_user
            ).distinct()

        last_name = self.request.GET.get("last_name")
        if last_name is not None and last_name is not "":
            queryset = queryset.filter(last_name__icontains=last_name)
        email = self.request.GET.get("email")
        if email is not None and email is not "":
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
    permission_classes = [IsAuthenticated, IsSalesOrManagerUser]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.user_type == "MNG":
            queryset = Contract.objects.all()
        else:
            clients = Client.objects.filter(sales_contact=current_user)
            queryset = Contract.objects.filter(client__in=clients)

        last_name = self.request.GET.get("last_name")
        if last_name is not None and last_name is not "":
            queryset = queryset.filter(client__last_name__icontains=last_name)

        email = self.request.GET.get("email")
        if email is not None and email is not "":
            queryset = queryset.filter(client__email__icontains=email)

        date_created = self.request.GET.get("date_created")
        if date_created is not None and date_created is not "":
            date_obj = datetime.strptime(date_created, "%d/%m/%Y")
            queryset = queryset.filter(date_created__date=date_obj)

        amount = self.request.GET.get("amount")
        if amount is not None and amount is not "":
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
    permission_classes = [IsAuthenticated, IsStaff]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.user_type == "MNG":
            queryset = Event.objects.all()
        elif current_user.user_type == "SLS":
            queryset = Event.objects.filter(client__sales_contact=current_user)
        elif current_user.user_type == "SPP":
            queryset = Event.objects.filter(support_contact=current_user)

        last_name = self.request.GET.get("last_name")
        if last_name is not None and last_name is not "":
            queryset = queryset.filter(client__last_name__icontains=last_name)

        email = self.request.GET.get("email")
        if email is not None and email is not "":
            queryset = queryset.filter(client__email__icontains=email)

        event_date = self.request.GET.get("event_date")
        if event_date is not None and event_date is not "":
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
