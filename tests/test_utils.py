# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from unittest import TestCase, skipIf

from gapipy.client import Client
from gapipy.resources.base import Resource
from gapipy.utils import (
    dict_to_model,
    duration_label,
    humanize_amount,
    humanize_price,
    humanize_time,
    location_label,
    enforce_string_type,
)


class UtilsTestCase(TestCase):

    def test_humanize_amount(self):
        self.assertEqual(humanize_amount('1'), '1')
        self.assertEqual(humanize_amount('1.5'), '1.50')
        self.assertEqual(humanize_amount('1.500'), '1.50')
        self.assertEqual(humanize_amount('0.50'), '0.50')
        self.assertEqual(humanize_amount('1', force_decimal=True), '1.00')

    def test_humanize_price_free(self):
        FREE = 'Free'
        self.assertEqual(humanize_price(0, None, 'CAD'), FREE)
        self.assertEqual(humanize_price(0.00, None, 'CAD'), FREE)
        self.assertEqual(humanize_price('0', None, 'CAD'), FREE)
        self.assertEqual(humanize_price('0.00', None, 'CAD'), FREE)
        self.assertEqual(humanize_price('0.00', 5.00, 'CAD'), 'Free-5CAD')

    def test_humanize_price_none(self):
        out = humanize_price(None, None, 'CAD')
        self.assertEqual(out, '')

    def test_humanize_price_range(self):
        self.assertEqual(humanize_price(1, 2, 'CAD'), '1-2CAD')
        self.assertEqual(humanize_price(2.5, 3.0, 'CAD'), '2.50-3.00CAD')
        self.assertEqual(humanize_price(2.5000, 3.1000, 'CAD'), '2.50-3.10CAD')
        # As strings
        self.assertEqual(humanize_price('2.5', '3.1', 'CAD'), '2.50-3.10CAD')

    def test_humanize_price_single(self):
        self.assertEqual(humanize_price(1, None, 'CAD'), '1CAD')
        self.assertEqual(humanize_price('1.50', None, 'CAD'), '1.50CAD')

    def test_humanize_time(self):
        self.assertEqual(humanize_time('1.5'), '1h30m')
        self.assertEqual(humanize_time('0.5'), '30m')
        self.assertEqual(humanize_time(1.0), '1h')

    def test_duration_label(self):
        self.assertEqual(duration_label(1.5, 2.5), '1h30m-2h30m')
        self.assertEqual(duration_label(1, None), '1h')
        self.assertEqual(duration_label('3.0', None), '3h')

    def test_location_label(self):
        import collections
        Place = collections.namedtuple('Place', ['name'])
        place_1 = Place(name='Toronto')
        place_2 = Place(name='Montreal')
        self.assertEqual(location_label(place_1, place_2), 'Toronto – Montreal')
        self.assertEqual(location_label(place_1, place_1), 'Toronto')

    def test_dict_to_model(self):
        data = {
            'id': '123',
            'name': {
                'first': 'Foo',
                'last': 'Baz',
                'reverse': {
                    'first': 'Oof',
                    'last': 'Zab',
                },
            },
            'phone_numbers': [
                {
                    'number': '555-555-5555',
                }

            ],
        }

        wrapper = dict_to_model('Profile')
        model = wrapper(data)

        self.assertEqual(str(model), 'Profile')
        self.assertEqual(repr(model), '<Profile>')
        self.assertEqual(model.id, '123')
        self.assertEqual(model.name.first, 'Foo')
        self.assertEqual(model.name.last, 'Baz')
        self.assertEqual(str(model.name), 'Name')

        self.assertEqual(model.name.reverse.first, 'Oof')
        self.assertEqual(model.name.reverse.last, 'Zab')

        self.assertEqual(str(model.phone_numbers[0]), 'Phone Numbers')
        self.assertEqual(model.phone_numbers[0].number, '555-555-5555')

    @skipIf(sys.version_info.major > 2, 'Only test for Python 2')
    def test_enforce_string_type(self):

        class MockResource(Resource):
            _as_is_fields = ['id', 'name']

            def __repr__(self):
                return '<{} {}>'.format(self.__class__.__name__, self.name)

        data = {
            'id': 123,
            'name': 'Alc\xe1zar Palace Visit',
        }
        client = Client()

        res = MockResource(data, client)

        with self.assertRaises(UnicodeEncodeError):
            s = repr(res)

        # Decorate `MockResource.__repr__` with `enforce_string_type`
        orig_repr = MockResource.__repr__
        MockResource.__repr__ = enforce_string_type(orig_repr)

        s = repr(res)  # doesn't raise UnicodeEncodeError
        self.assertIsInstance(s, str)
        self.assertNotIsInstance(s, unicode)
        self.assertEqual(s, b'<MockResource Alcázar Palace Visit>')
