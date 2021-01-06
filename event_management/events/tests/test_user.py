import factory
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from event_management.events.models import User
from event_management.events.tests.factories import UserFactory

faker = Faker()


class UserDict(dict):
    def set_password(self, value: str) -> None:
        super().__setitem__("password", value)
        super().__setitem__("raw_password", value)


class UserTest(APITestCase):
    def test_create_new_user(self):
        data = factory.build(UserDict, FACTORY_CLASS=UserFactory)

        response = self.client.post("/users/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.get(email=data["email"])
        self.assertTrue(created_user.has_usable_password())
