"""Tests for the extension seams on `Client`.

Covers:
- `register_resource` / `get_resource_class_by_name` (ticket 02)
- `on_response` (ticket 03)
- `register_config_defaults` (ticket 03)
"""
import unittest
from unittest import mock

import requests_mock

from gapipy import client as client_module
from gapipy.client import Client, default_config
from gapipy.resources.base import Resource


class FakeResource(Resource):
    _resource_name = "fakes"
    _as_is_fields = ["id", "name"]


class OverrideBooking(Resource):
    _resource_name = "bookings"
    _as_is_fields = ["id"]


class RegisterResourceTests(unittest.TestCase):

    def test_register_and_lookup_by_class_name(self):
        c = Client()
        c.register_resource(FakeResource)
        self.assertIs(c.get_resource_class_by_name("FakeResource"), FakeResource)

    def test_register_and_lookup_by_resource_name(self):
        c = Client()
        c.register_resource(FakeResource)
        self.assertIs(c.get_resource_class_by_name("fakes"), FakeResource)

    def test_instance_registration_wins_over_module_default(self):
        c = Client()
        # `bookings` resolves to the built-in Booking through the module registry;
        # after instance registration it must resolve to our override.
        c.register_resource(OverrideBooking)
        self.assertIs(c.get_resource_class_by_name("bookings"), OverrideBooking)

    def test_unregistered_name_raises(self):
        c = Client()
        with self.assertRaises(KeyError):
            c.get_resource_class_by_name("NoSuchResource")

    def test_builtins_registered_at_init(self):
        c = Client()
        # A representative built-in
        self.assertIsNotNone(c.get_resource_class_by_name("Tour"))
        self.assertIsNotNone(c.get_resource_class_by_name("tours"))


class OnResponseTests(unittest.TestCase):

    def test_callback_fires_on_200(self):
        c = Client(api_root="https://api.example.com")
        seen = []
        c.on_response(lambda resp: seen.append(resp.status_code))
        with requests_mock.Mocker() as m:
            m.get("https://api.example.com/tours/1", json={"id": 1})
            c.tours.get(1)
        self.assertEqual(seen, [200])

    def test_callback_fires_on_4xx(self):
        c = Client(api_root="https://api.example.com")
        seen = []
        c.on_response(lambda resp: seen.append(resp.status_code))
        with requests_mock.Mocker() as m:
            m.get("https://api.example.com/tours/1", status_code=404, text="not found")
            try:
                c.tours.get(1)
            except Exception:
                pass
        self.assertEqual(seen, [404])

    def test_multiple_callbacks_fire_in_registration_order(self):
        c = Client(api_root="https://api.example.com")
        order = []
        c.on_response(lambda resp: order.append("first"))
        c.on_response(lambda resp: order.append("second"))
        with requests_mock.Mocker() as m:
            m.get("https://api.example.com/tours/1", json={"id": 1})
            c.tours.get(1)
        self.assertEqual(order, ["first", "second"])

    def test_callback_sees_redirect_history(self):
        c = Client(api_root="https://api.example.com")
        seen_history_lengths = []
        c.on_response(lambda resp: seen_history_lengths.append(len(resp.history)))
        with requests_mock.Mocker() as m:
            m.get("https://api.example.com/tours/1", status_code=303, headers={"Location": "https://api.example.com/tours/2"})
            m.get("https://api.example.com/tours/2", json={"id": 2})
            c.tours.get(1)
        self.assertEqual(seen_history_lengths, [1])


class RegisterConfigDefaultsTests(unittest.TestCase):

    def setUp(self):
        self._snapshot = dict(default_config)

    def tearDown(self):
        default_config.clear()
        default_config.update(self._snapshot)

    def test_new_default_applied_to_future_clients(self):
        Client.register_config_defaults({"booking_company_id": 42})
        c = Client()
        # Merged into default_config, so get_config resolves it.
        self.assertEqual(client_module.get_config({}, "booking_company_id"), 42)

    def test_does_not_retroactively_mutate_existing_clients(self):
        c_before = Client()
        # snapshot a config attribute that clients read at __init__
        old_api_root = c_before.api_root
        Client.register_config_defaults({"api_root": "https://elsewhere.example.com"})
        # existing client's attributes are unchanged
        self.assertEqual(c_before.api_root, old_api_root)
        # a new client picks up the new default
        c_after = Client()
        self.assertEqual(c_after.api_root, "https://elsewhere.example.com")


if __name__ == "__main__":
    unittest.main()
