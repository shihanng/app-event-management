from rest_framework import serializers

from event_management.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:  # pylint: disable=R0903
        model = Event
        fields = ["name", "location", "uuid", "start_time", "end_time"]
        read_only_fields = ["uuid"]
