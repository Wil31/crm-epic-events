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


class ContractViewset(ReadOnlyModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = []

    def get_queryset(self):
        return Contract.objects.all()


class EventViewset(ReadOnlyModelViewSet):

    serializer_class = EventSerializer
    permission_classes = []

    def get_queryset(self):
        return Event.objects.all()
