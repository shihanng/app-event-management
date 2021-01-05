from django.contrib.auth import password_validation

from rest_framework import serializers

from event_management.events.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # pylint: disable=R0903
        model = User
        fields = ["email"]

    def validate_password(self, value):  # pylint: disable=R0201
        password_validation.validate_password(value)

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
