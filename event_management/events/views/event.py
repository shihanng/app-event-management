from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from event_management.events.models import Event
from event_management.events.serializers import EventSerializer


class EventViewSet(ModelViewSet):  # pylint: disable=R0901
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "uuid"
