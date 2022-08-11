from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer


class ClientViewset(ReadOnlyModelViewSet):

    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.all()


class ContractViewset(ReadOnlyModelViewSet):

    serializer_class = ContractSerializer

    def get_queryset(self):
        return Contract.objects.all()


class EventViewset(ReadOnlyModelViewSet):

    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()
