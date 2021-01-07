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

        if event.user.filter(email=request.user.email).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        event.user.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["put"])
    def deregister(self, request, *args, **kwargs):
        event = self.get_object()

        if not event.user.filter(email=request.user.email).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        event.user.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
