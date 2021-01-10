import logging

from django.conf import settings
from django.core.mail import send_mail

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from event_management.events.models import Event
from event_management.events.serializers import EmptySerializer, EventSerializer

logger = logging.getLogger(__name__)


class EventViewSet(ModelViewSet):  # pylint: disable=R0901
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action == "register" or self.action == "deregister":
            return EmptySerializer
        return EventSerializer

    @swagger_auto_schema(
        operation_description="Signup current logged in user to the event"
    )
    @action(detail=True, methods=["put"])
    def register(self, request, *args, **kwargs):  # pylint: disable=W0613
        event = self.get_object()

        if event.user.filter(email=request.user.email).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        event.user.add(request.user)

        if settings.NOTIFY_TO:
            send_mail(
                f'New registration for event "{event.name}"',
                f"{request.user.email} has registered.",
                settings.EMAIL_HOST_USER,
                [settings.NOTIFY_TO],
                fail_silently=False,
            )
        else:
            logger.warning("skip email notification because EMAIL_HOST_USER not set")

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Remove current logged in user from the event"
    )
    @action(detail=True, methods=["put"])
    def deregister(self, request, *args, **kwargs):  # pylint: disable=W0613
        event = self.get_object()

        if not event.user.filter(email=request.user.email).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        event.user.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # pylint: disable=C0103
    @swagger_auto_schema(
        operation_description="List all events of current logged in user"
    )
    @action(detail=False, methods=["get"])
    def me(self, request):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
