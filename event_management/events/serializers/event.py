from typing import List

from rest_framework import serializers

from event_management.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["name", "location", "uuid", "start_time", "end_time"]
        read_only_fields = ["uuid"]

    def validate(self, attrs):
        if attrs["start_time"] > attrs["end_time"]:
            raise serializers.ValidationError("start_time must come before end_time")
        return attrs


class EmptySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields: List[str] = []
