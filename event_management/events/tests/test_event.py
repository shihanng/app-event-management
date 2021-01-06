import factory
from rest_framework import status
from rest_framework.test import APITestCase

from event_management.events.tests.factories import EventFactory, UserFactory


class EventTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)

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
