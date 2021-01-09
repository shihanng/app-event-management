from django.test import override_settings
from django.utils.timezone import utc

import factory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from event_management.events.models import EventUser
from event_management.events.tests.factories import EventFactory, UserFactory


class EventTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_create_event(self):
        data = factory.build(dict, FACTORY_CLASS=EventFactory, uuid=None)

        data.update(
            {
                "start_time": data["start_time"].isoformat(),
                "end_time": data["end_time"].isoformat(),
            }
        )

        response = self.client.post("/events/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        uuid = response.data["uuid"]
        response = self.client.get(f"/events/{uuid}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event_validate(self):
        data = factory.build(
            dict,
            FACTORY_CLASS=EventFactory,
            uuid=None,
            start_time=factory.Faker("future_datetime", tzinfo=utc),
            end_time=factory.Faker("past_datetime", tzinfo=utc),
        )

        data.update(
            {
                "start_time": data["start_time"].isoformat(),
                "end_time": data["end_time"].isoformat(),
            }
        )

        response = self.client.post("/events/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(NOTIFY_TO="test@example.com")
    def test_register_deregister_event(self):
        event = EventFactory()

        response = self.client.put(f"/events/{event.uuid}/register/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(r"/events/me/")
        self.assertContains(
            response,
            event.uuid,
            status_code=status.HTTP_200_OK,
        )

        response = self.client.put(f"/events/{event.uuid}/register/")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.put(f"/events/{event.uuid}/deregister/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(EventUser.DoesNotExist):
            EventUser.objects.get(user__email=self.user.email, event__uuid=event.uuid)

        response = self.client.put(f"/events/{event.uuid}/deregister/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
