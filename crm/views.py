from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from .permissions import IsSalesAuthenticated


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [IsSalesAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return Client.objects.filter(sales_contact=current_user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Client '{instance}' deleted successfully."},
            status=status.HTTP_200_OK,
        )


class ContractViewset(ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [IsSalesAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
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
    permission_classes = [IsSalesAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        clients = Client.objects.filter(sales_contact=current_user)
        return Event.objects.filter(client__in=clients)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Event '{instance}' deleted successfully."},
            status=status.HTTP_200_OK,
        )
