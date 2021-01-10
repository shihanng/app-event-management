from typing import Any, Sequence

from django.contrib.auth import get_user_model
from django.utils.timezone import utc

from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    is_staff = Faker("boolean")

    def __init__(self):
        self.raw_password = ""

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        self.raw_password = (
            extracted
            if extracted
            else Faker._get_faker().password(
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(self.raw_password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]


class EventFactory(DjangoModelFactory):
    name = Faker("catch_phrase")
    location = Faker("city")
    uuid = Faker("uuid4")
    start_time = Faker("past_datetime", tzinfo=utc)
    end_time = Faker("future_datetime", tzinfo=utc)

    class Meta:
        model = "events.Event"
