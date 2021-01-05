from django.apps import apps
from django.test import TestCase

from event_management.events.apps import EventsConfig


class EventsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(EventsConfig.name, "event_management.events")
        self.assertEqual(apps.get_app_config("events").name, "event_management.events")

    def test_default_app_config(self):
        with self.settings(
            INSTALLED_APPS=["event_management.events.apps.EventsConfig"]
        ):
            config = apps.get_app_config("events")
            self.assertIsInstance(config, EventsConfig)
