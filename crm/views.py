from http import client
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
            return Client.objects.all()
        elif current_user.user_type == "SLS":
            return Client.objects.filter(sales_contact=current_user)
        elif current_user.user_type == "SPP":
            events = Event.objects.filter(support_contact=current_user)
            clients = []
            for event in events:
                clients.append(event.client)
            clients = list(dict.fromkeys(clients))
            return clients

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
            return Contract.objects.all()
        else:
            clients = Client.objects.filter(sales_contact=current_user)
            return Contract.objects.filter(client__in=clients)

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
            return Event.objects.all()
        elif current_user.user_type == "SLS":
            clients = Client.objects.filter(sales_contact=current_user)
            return Event.objects.filter(client__in=clients)
        elif current_user.user_type == "SPP":
            return Event.objects.filter(support_contact=current_user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Event '{instance}' deleted successfully."},
            status=status.HTTP_200_OK,
        )
