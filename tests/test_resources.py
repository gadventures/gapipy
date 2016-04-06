# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import sys
from unittest import TestCase, skipIf

from mock import patch

from gapipy.client import Client
from gapipy.query import Query
from gapipy.models import DATE_FORMAT, AccommodationRoom
from gapipy.resources import (
    Departure,
    Promotion,
    Tour,
    TourDossier,
    ActivityDossier,
)
from gapipy.resources.base import Resource

from .fixtures import DUMMY_DEPARTURE, PPP_TOUR_DATA, PPP_DOSSIER_DATA


class ResourceTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_to_dict(self):
        t = Tour(PPP_TOUR_DATA, client=self.client)
        self.assertEquals(t.to_dict(), PPP_TOUR_DATA)

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
        self.assertEquals(data['date_field'], '2013-02-18')
        self.assertEquals(data['date_field_utc'], '2013-02-18T18:17:20Z')

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
        self.assertEquals(t.id, 1)

        self.assertTrue(isinstance(t.tour_dossier, TourDossier))
        self.assertTrue(isinstance(t.departures, Query))

        # Force a fetch.
        assert t.departures_start_date

        mock_fetch.assert_called_once()
        self.assertFalse(t.is_stub)
        self.assertEquals(
            t.departures_start_date,
            datetime.datetime.strptime('2013-01-01', DATE_FORMAT).date()
        )
        self.assertEquals(
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

        self.assertEquals(f.to_dict(), {
            'bar': {'id': 1, 'date': '2013-01-01'}
        })
        self.assertIsInstance(f.bar, Bar)
        self.assertEquals(f.bar.id, 1)
        self.assertEquals(f.bar.date, datetime.date(2013, 01, 01))

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

        self.assertEquals(f.bar, None)

    @skipIf(sys.version_info.major > 2, 'Only test for Python 2')
    def test_repr_returns_bytes_in_python2(self):
        data = {
            'id': 123,
            'name': 'Alc\xe1zar Palace Visit',
        }
        ad = ActivityDossier(data, self.client)
        s = repr(ad)
        self.assertIsInstance(s, str)
        self.assertNotIsInstance(s, unicode)
        self.assertEqual(s, b'<ActivityDossier Alcázar Palace Visit>')


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
