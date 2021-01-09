from typing import List

from rest_framework import serializers

from event_management.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:  # pylint: disable=R0903
        model = Event
        fields = ["name", "location", "uuid", "start_time", "end_time"]
        read_only_fields = ["uuid"]

    def validate(self, data):
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError("start_time must come before end_time")
        return data


class EmptySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields: List[str] = []
