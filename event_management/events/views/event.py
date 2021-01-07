from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from event_management.events.models import Event
from event_management.events.serializers import EmptySerializer, EventSerializer


class EventViewSet(ModelViewSet):  # pylint: disable=R0901
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action == "register" or self.action == "deregister":
            return EmptySerializer
        return EventSerializer

    @action(detail=True, methods=["put"])
    def register(self, request, *args, **kwargs):
        event = self.get_object()
        event.user.add(request.user)

        # TODO(shihanng): Check if already registered

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["put"])
    def deregister(self, request, *args, **kwargs):
        event = self.get_object()
        event.user.remove(request.user)

        # TODO(shihanng): Check if already deregistered

        return Response(status=status.HTTP_204_NO_CONTENT)
