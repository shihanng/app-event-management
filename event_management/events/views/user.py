from rest_framework.viewsets import ModelViewSet
from event_management.events.models import User
from event_management.events.serializers import UserSerializer


class UserViewSet(ModelViewSet):  # pylint: disable=R0901
    queryset = User.objects.all()
    serializer_class = UserSerializer
