# -*- coding: utf-8 -*-
# Python 2 and 3
from __future__ import unicode_literals

import datetime
import sys
from unittest import TestCase

from mock import patch

from gapipy.client import Client
from gapipy.query import Query
from gapipy.models import DATE_FORMAT, AccommodationRoom
from gapipy.resources import (
    ActivityDossier,
    Departure,
    Itinerary,
    Promotion,
    Tour,
    TourDossier,
)
from gapipy.resources.base import Resource
from gapipy.resources.tour.itinerary import ValidDuringRange

from .fixtures import DUMMY_DEPARTURE, PPP_TOUR_DATA, PPP_DOSSIER_DATA


class ResourceTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_to_dict(self):
        t = Tour(PPP_TOUR_DATA, client=self.client)
        self.assertEqual(t.to_dict(), PPP_TOUR_DATA)

    def test_to_dict_datetimes(self):
        class DatetimeResource(Resource):
            _as_is_fields = ['id']
            _date_fields = ['date_field']
            _date_time_fields_utc = ['date_field_utc']

        resource = DatetimeResource({
            'id': 1,
            'date_field': '2013-02-18',
            'date_field_utc': '2013-02-18T18:17:20Z',
        }, client=self.client)
        data = resource.to_dict()
        self.assertEqual(data['date_field'], '2013-02-18')
        self.assertEqual(data['date_field_utc'], '2013-02-18T18:17:20Z')

    @patch('gapipy.request.APIRequestor._request', return_value=PPP_DOSSIER_DATA)
    def test_instantiate_from_raw_data(self, mock_request):
        t = Tour(PPP_TOUR_DATA, client=self.client)
        self.assertIsInstance(t, Tour)
        self.assertEqual(t.product_line, 'PPP')
        self.assertIsInstance(t.departures_start_date, datetime.date)
        self.assertIsInstance(t.tour_dossier, TourDossier)
        self.assertIsInstance(t.departures, Query)

    @patch('gapipy.request.APIRequestor._request')
    def test_populate_stub(self, mock_fetch):
        mock_fetch.return_value = {
            'id': 1,
            'product_line': 'PPP',
            'href': '/1',
            'departures_start_date': '2013-01-01',
            'departures_end_date': '2014-01-01',
            'tour_dossier': {
                'id': 1,
            },
            'departures': [
                {'id': 1},
                {'id': 2},
            ],
        }
        data = {'id': 1, 'product_line': 'PPP'}

        t = Tour(data, client=self.client, stub=True)
        self.assertTrue(t.is_stub)
        self.assertEqual(t.id, 1)

        self.assertTrue(isinstance(t.tour_dossier, TourDossier))
        self.assertTrue(isinstance(t.departures, Query))

        # Force a fetch.
        assert t.departures_start_date

        mock_fetch.assert_called_once()
        self.assertFalse(t.is_stub)
        self.assertEqual(
            t.departures_start_date,
            datetime.datetime.strptime('2013-01-01', DATE_FORMAT).date()
        )
        self.assertEqual(
            t.departures_end_date,
            datetime.datetime.strptime('2014-01-01', DATE_FORMAT).date()
        )

    def test_model_fields(self):
        from gapipy.models.base import BaseModel

        class Bar(BaseModel):
            _as_is_fields = ['id']
            _date_fields = ['date']

        class Foo(Resource):
            _model_fields = [('bar', Bar)]

        data = {
            'bar': {
                'id': 1,
                'date': '2013-01-01',
            }
        }
        f = Foo(data, client=self.client)

        self.assertEqual(f.to_dict(), {
            'bar': {'id': 1, 'date': '2013-01-01'}
        })
        self.assertIsInstance(f.bar, Bar)
        self.assertEqual(f.bar.id, 1)
        self.assertEqual(f.bar.date, datetime.date(2013, 0o1, 0o1))

    def test_null_model_fields(self):
        from gapipy.models.base import BaseModel

        class Bar(BaseModel):
            _as_is_fields = ['id']
            _date_fields = ['date']

        class Foo(Resource):
            _model_fields = [('bar', Bar)]

        data = {
            'bar': None
        }
        f = Foo(data, client=self.client)

        self.assertEqual(f.bar, None)


class AccommodationRoomTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_room_class_is_set_properly(self):
        data = {
            'code': 1234,
            'min_nights': 1,
            'max_nights': 2,
            'price_bands': [],
            'class': 'Standard',
        }
        room = AccommodationRoom(data, client=self.client)
        self.assertEqual(room.room_class, 'Standard')

    def test_room_class_is_set_properly_when_cached(self):
        data = {
            'code': 1234,
            'min_nights': 1,
            'max_nights': 2,
            'price_bands': [],
            'room_class': 'Standard',
        }
        room = AccommodationRoom(data, client=self.client)
        self.assertEqual(room.room_class, 'Standard')


class PromotionTestCase(TestCase):
    @patch('gapipy.request.APIRequestor._request')
    def test_product_type_is_set_properly(self, mock_request):
        data = {
            'products': [
                {
                    'type': 'departures',
                    'sub_type': 'Tour',
                    'id': 1,
                }
            ],
        }

        promotion = Promotion(data, client=Client())
        product = promotion.products[0]
        self.assertEqual(product.type, 'departures')
        self.assertEqual(product.to_dict(), {
            'id': 1,
            'type': 'departures',
            'sub_type': 'Tour',
        })

        # Ensure when the product implicitly fetched it makes a request, and
        # retains the type fields.
        self.assertEqual(mock_request.call_count, 0)
        mock_request.return_value = {
            'finish_address': {
                'country': {
                    'name': 'Australia',
                }
            }
        }
        self.assertEqual(product.finish_address.country.name, 'Australia')
        self.assertEqual(product.type, 'departures')


class PricePromotionTestCase(TestCase):
    def test_fake_amount_is_set_properly(self):
        departure = Departure(DUMMY_DEPARTURE, client=Client())
        prices = departure.rooms[0].price_bands[0].prices
        for price in prices:
            promotion = price.promotions[0].to_dict()
            self.assertTrue('amount' in promotion)


class DepartureAddonTestCase(TestCase):
    """
    Test that the departures.addons.product instances get appropriate resource
    types.

    This is a regression test for some erroneous behaviour of the AddOn model.

    The AddOn._resource_fields list was defined at the class level, and as-such
    it was shared among intances of that class. The effect is that if you have
    three addons, they will all be using the same model for their "product"
    even when those products are different type (e.g. "accommodations" versus
    "activities" versus "transports" versus "single_supplements" etc.)

    Desired behaviour is that each AddOn.product is represented by a model
    appropriate for its type.
    """
    def test_departure_addon_product_types(self):
        departure = Departure(DUMMY_DEPARTURE, client=Client())

        for addon in departure.addons:

            # Product should use a resource class that matches with its type
            self.assertEqual(addon.product._resource_name, addon.product.type)

            # Each addon instance should have only one resource class listed
            # for it's "product" field
            product_resource_fields = [
                (field, resource_class)
                for (field, resource_class) in addon._resource_fields
                if field == 'product']
            self.assertEqual(len(product_resource_fields), 1)


def build_vrange(start, end):
    """
    Returns a ValidDuringRange instance, given a start and end `date`

    We take care of formatting the `date` object as a string, and we just
    set the `client` argument to `None` because we don't need access to the
    API to test the validity functionality.
    """
    return ValidDuringRange({
        'start_date': start.isoformat() if start else None,
        'end_date': end.isoformat() if end else None,
    }, None)


class ValidDuringRangeTestCase(TestCase):
    """ Tests the date-range-checking logic on
    resources.tour.itinerary.ValidDuringRange
    """

    def test_is_valid_during_range__start(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # We'll be testing with a range that defines a start-date and no end...
        test_range = (today, None)

        # Check a range that falls entirely before our test_range
        self.assertFalse(
            build_vrange(today - (2 * a_week), today - a_week).is_valid_during_range(*test_range))

        # Check a range that falls before and overlapping our test_range
        self.assertTrue(
            build_vrange(today - a_week, today + a_week).is_valid_during_range(*test_range))

        # Check a range contained by our test_range
        self.assertTrue(
            build_vrange(today + a_week, today + (2 * a_week)).is_valid_during_range(*test_range))

        # Some cases we cannot check, because our test_range has no end:
        # - a range that contains our test_range
        # - a range that overlaps and falls after our test_range
        # - a range that falls entirely after our test_range

    def test_is_valid_during_range__end(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # We'll be testing with a range that defines an end-date and no start...
        test_range = (None, today)

        # Check a range contained by our test_range
        self.assertTrue(
            build_vrange(today - (2 * a_week), today - a_week).is_valid_during_range(*test_range))

        # Check a range that overlaps and falls after our test_range
        self.assertTrue(
            build_vrange(today - a_week, today + a_week).is_valid_during_range(*test_range))

        # Check a range that falls entirely after our test_range
        self.assertFalse(
            build_vrange(today + a_week, today + (2 * a_week)).is_valid_during_range(*test_range))

        # Some cases we cannot check, because our test_range has no start:
        # - a range that falls entirely before our test_range
        # - a range that falls before and overlapping our test_range
        # - a range that contains our test_range

    def test_is_valid_during_range__start_end(self):
        today = datetime.date.today()
        a_day = datetime.timedelta(1)
        a_week = datetime.timedelta(7)

        # We'll be testing with a range that defines both a start and end date
        test_range = (today, today + a_week)

        # Check ranges that fall entirely before our test_range
        self.assertFalse(
            build_vrange(today - (2 * a_week), today - a_week).is_valid_during_range(*test_range))
        self.assertFalse(
            build_vrange(None, today - a_week).is_valid_during_range(*test_range))

        # Check a range that falls before and overlapping our test_range
        self.assertTrue(
            build_vrange(today - (2 * a_week), today).is_valid_during_range(*test_range))

        # Check a range that contains our test_range
        self.assertTrue(
            build_vrange(today - (2 * a_week), today + (2 * a_week)).is_valid_during_range(*test_range))

        # Check a range contained by our test_range
        self.assertTrue(
            build_vrange(today + a_day, today + a_week - a_day).is_valid_during_range(*test_range))

        # Check a range that overlaps and falls after our test_range
        self.assertTrue(
            build_vrange(today + a_day, today + (2 * a_week)).is_valid_during_range(*test_range))

        # Check ranges that fall entirely after our test_range
        self.assertFalse(
            build_vrange(today + (2 * a_week), today + (3 * a_week)).is_valid_during_range(*test_range))
        self.assertFalse(
            build_vrange(today + (2 * a_week), None).is_valid_during_range(*test_range))

    def test_is_valid_during_range__none(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # We'll be testing with a range that defines neither start or end
        # date... this should be equivalent to the is_valid_sometime call..
        test_range = (None, None)

        # Check a range that contains our test_range
        self.assertTrue(
            build_vrange(None, None).is_valid_during_range(*test_range))

        # Check a range contained by our test_range
        self.assertTrue(
            build_vrange(today, None).is_valid_during_range(*test_range))
        self.assertTrue(
            build_vrange(None, today).is_valid_during_range(*test_range))
        self.assertTrue(
            build_vrange(today - a_week, today).is_valid_during_range(*test_range))

        # Some cases we cannot check, because our test_range is (None, None):
        # - a range that falls entirely before our test_range
        # - a range that falls before and overlapping our test_range
        # - a range that overlaps and falls after our test_range
        # - a range that falls entirely after our test_range

    def test_is_valid_during_range__invalid(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # We'll be testing with a range that starts after it ends (so, NOTHING
        # should be valid in this range)
        test_range = (today, today - a_week)

        self.assertFalse(
            build_vrange(today, None).is_valid_during_range(*test_range))
        self.assertFalse(
            build_vrange(None, today).is_valid_during_range(*test_range))
        self.assertFalse(
            build_vrange(today - a_week, today).is_valid_during_range(*test_range))

    def test_is_valid_on_or_after_date(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # Check a range that is valid ON the date in question (but not AFTER the date)
        self.assertTrue(
            build_vrange(today, today).is_valid_on_or_after_date(today))

        # Check a range that is valid AFTER the date in question (but not ON the date)
        self.assertTrue(
            build_vrange(today + a_week, None).is_valid_on_or_after_date(today))

        # Check some ranges that are valid before, on, AND after the date in question
        self.assertTrue(
            build_vrange(None, None).is_valid_on_or_after_date(today))
        self.assertTrue(
            build_vrange(today - a_week, None).is_valid_on_or_after_date(today))

        # Check some ranges (closed and half-open) that are not valid after or on the date
        self.assertFalse(
            build_vrange(today - (2 * a_week), today - a_week).is_valid_on_or_after_date(today))
        self.assertFalse(
            build_vrange(None, today - a_week).is_valid_on_or_after_date(today))

    def test_is_valid_on_or_before_date(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # Check a range that is valid ON the date in question (but not BEFORE the date)
        self.assertTrue(
            build_vrange(today, today).is_valid_on_or_before_date(today))

        # Check a range that is valid BEFORE the date in question (but not ON the date)
        self.assertTrue(
            build_vrange(None, today - a_week).is_valid_on_or_before_date(today))

        # Check some ranges that are valid before, on, AND after the date in question
        self.assertTrue(
            build_vrange(None, None).is_valid_on_or_before_date(today))
        self.assertTrue(
            build_vrange(today - a_week, None).is_valid_on_or_before_date(today))

        # Check some ranges (closed and half-open) that are not valid before or on the date
        self.assertFalse(
            build_vrange(today + a_week, today + (2 * a_week)).is_valid_on_or_before_date(today))
        self.assertFalse(
            build_vrange(today + a_week, None).is_valid_on_or_before_date(today))

    def test_is_valid_on_date(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        invalid_range_closed = build_vrange(today - (2 * a_week), today - a_week)
        self.assertFalse(invalid_range_closed.is_valid_on_date(today))

        invalid_range_half_open = build_vrange(today + (2 * a_week), None)
        self.assertFalse(invalid_range_half_open.is_valid_on_date(today))

        valid_range_closed = build_vrange(today - (2 * a_week), today + a_week)
        self.assertTrue(valid_range_closed.is_valid_on_date(today))

        valid_range_half_open = build_vrange(None, today + a_week)
        self.assertTrue(valid_range_half_open.is_valid_on_date(today))

        valid_range_open = build_vrange(None, None)
        self.assertTrue(valid_range_open.is_valid_on_date(today))

    def test_is_valid_sometime(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # A range that starts after it finishes is never valid
        invalid_range = build_vrange(today + a_week, today - a_week)
        self.assertFalse(invalid_range.is_valid_sometime())

        # Otherwise, it's valid sometime if there is a start...
        self.assertTrue(build_vrange(today, None).is_valid_sometime())

        # ... or end ...
        self.assertTrue(build_vrange(None, today).is_valid_sometime())

        # ... or both (where start >= end)
        self.assertTrue(build_vrange(today + a_week, today + a_week).is_valid_sometime())


class ItineraryValidityTestCase(TestCase):
    """ Tests the date-range-checking logic on
    resources.tour.itinerary.Itinerary
    """
    def build_itin(self, ranges):
        """
        Returns an Itinerary instance, given a list of (start, end) `date`
        tuples to be used to populate the list of `valid_during_ranges`.
        """
        ranges = ranges or []
        return Itinerary({
            'id': 'who cares',
            'valid_during_ranges': [
                {
                    'start_date': start.isoformat() if start else None,
                    'end_date': end.isoformat() if end else None,
                } for (start, end) in ranges
            ],
        }, None)

    def test_is_expired(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # Check no ranges
        self.assertTrue(self.build_itin(None).is_expired())

        # Check one expired
        self.assertTrue(
            self.build_itin([
                (today - (2 * a_week), today - a_week),
            ]).is_expired()
        )

        # Check one expired, one valid
        self.assertFalse(
            self.build_itin([
                (today - (2 * a_week), today - a_week),
                (today, today + a_week),
            ]).is_expired()
        )

        # Check one valid
        self.assertFalse(
            self.build_itin([
                (today, today + a_week),
            ]).is_expired()
        )

    def test_is_valid_during_range(self):
        today = datetime.date.today()
        a_day = datetime.timedelta(1)
        a_week = datetime.timedelta(7)

        test_range = (today + a_day, today + a_day + a_week)

        # Check no ranges
        self.assertFalse(self.build_itin(None).is_valid_during_range(*test_range))

        # Check one invalid
        self.assertFalse(
            self.build_itin([
                (today - a_week, today),
            ]).is_valid_during_range(*test_range)
        )

        # Check one invalid, one valid
        self.assertTrue(
            self.build_itin([
                (today - a_week, today),
                (today, today + a_week),
            ]).is_valid_during_range(*test_range)
        )

        # Check one valid
        self.assertTrue(
            self.build_itin([
                (today, today + a_week),
            ]).is_valid_during_range(*test_range)
        )

    def test_is_valid_on_or_after_date(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # Check no ranges
        self.assertFalse(self.build_itin(None).is_valid_on_or_after_date(today))

        # Check one invalid
        self.assertFalse(
            self.build_itin([
                (today - (2 * a_week), today - a_week),
            ]).is_valid_on_or_after_date(today)
        )

        # Check one invalid, one valid
        self.assertTrue(
            self.build_itin([
                (today + a_week, today + (2 * a_week)),
                (today - (2 * a_week), today - a_week),
            ]).is_valid_on_or_after_date(today)
        )

        # Check one valid
        self.assertTrue(
            self.build_itin([
                (today + a_week, today + (2 * a_week)),
            ]).is_valid_on_or_after_date(today)
        )

    def test_is_valid_on_or_before_date(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # Check no ranges
        self.assertFalse(self.build_itin(None).is_valid_on_or_before_date(today))

        # Check one invalid
        self.assertFalse(
            self.build_itin([
                (today + a_week, today + (2 * a_week)),
            ]).is_valid_on_or_before_date(today)
        )

        # Check one invalid, one valid
        self.assertTrue(
            self.build_itin([
                (today + a_week, today + (2 * a_week)),
                (today - (2 * a_week), today - a_week),
            ]).is_valid_on_or_before_date(today)
        )

        # Check one valid
        self.assertTrue(
            self.build_itin([
                (today - (2 * a_week), today - a_week),
            ]).is_valid_on_or_before_date(today)
        )

    def test_is_valid_on_date(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # Check no ranges
        self.assertFalse(self.build_itin(None).is_valid_on_date(today))

        # Check one invalid
        self.assertFalse(
            self.build_itin([
                (today - (2 * a_week), today - a_week),
            ]).is_valid_on_date(today)
        )

        # Check one invalid, one valid
        self.assertTrue(
            self.build_itin([
                (today - (2 * a_week), today - a_week),
                (today, today + a_week),
            ]).is_valid_on_date(today)
        )

        # Check one valid
        self.assertTrue(
            self.build_itin([
                (today, today + a_week),
            ]).is_valid_on_date(today)
        )

    def test_is_valid_sometime(self):
        today = datetime.date.today()
        a_week = datetime.timedelta(7)

        # Check no ranges
        self.assertFalse(self.build_itin(None).is_valid_sometime())

        # Check one invalid (note start is after finish)
        self.assertFalse(
            self.build_itin([
                (today - a_week, today - (2 * a_week)),
            ]).is_valid_sometime()
        )

        # Check one invalid, one valid
        self.assertTrue(
            self.build_itin([
                (today - a_week, today - (2 * a_week)),
                (today, today + a_week),
            ]).is_valid_sometime()
        )

        # Check one valid
        self.assertTrue(
            self.build_itin([
                (today, today + a_week),
            ]).is_valid_sometime()
        )
