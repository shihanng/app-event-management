from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from event_management.events.models import User
from event_management.events.serializers import UserSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):  # pylint: disable=R0901
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
