from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from .permissions import IsSalesAuthenticated


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [IsSalesAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return Client.objects.filter(sales_contact=current_user)


class ContractViewset(ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [IsSalesAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        clients = Client.objects.filter(sales_contact=current_user)
        return Contract.objects.filter(client__in=clients)


class EventViewset(ReadOnlyModelViewSet):

    serializer_class = EventSerializer
    permission_classes = []

    def get_queryset(self):
        return Event.objects.all()
