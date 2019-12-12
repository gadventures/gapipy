# -*- coding: utf-8 -*-
# Python 2 and 3
from __future__ import unicode_literals

import sys
from unittest import TestCase

from gapipy.client import Client
from gapipy.resources.base import Resource
from gapipy.utils import (
    duration_label,
    humanize_amount,
    humanize_price,
    humanize_time,
    location_label,
    enforce_string_type,
    compute_request_signature,
    compute_webhook_validation_key,
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

    def test_compute_request_signature_handles_unicode_and_str(self):
        """
        Test that compute_request_signature doesn't explode when given both unicode
        and str inputs.
        NOTE: All this test does is validate that calling the method does not raise an
        exception for the different scenarios.
        """
        # Matching types for both args
        compute_request_signature(str('str app key'), str('str request body'))
        compute_request_signature(u'unicode app key', u'unicode request body')

        # Mismatched types for the args
        compute_request_signature(str('str app key'), u'unicode request body')
        compute_request_signature(u'unicode app key', str('str request body'))

        # Including special characters (really this should never come up for the
        # app key... should only contain digits and a-f as it is a hex string)
        compute_request_signature(str('str app key'), u'ʎpoq ʇsǝnbǝɹ ǝpoɔᴉun')
        compute_request_signature(u'ʎǝʞ ddɐ ǝpoɔᴉun', str('str request body'))
        compute_request_signature(u'ʎǝʞ ddɐ ǝpoɔᴉun', u'ʎpoq ʇsǝnbǝɹ ǝpoɔᴉun')

    def test_compute_webhook_validation_key_handles_unicode_and_str(self):
        """
        Test that compute_webhook_validation_key doesn't explode when given unicode
        or str input.
        NOTE: All this test does is validate that calling the method does not raise an
        exception for the different scenarios.
        """
        # Bytestring/Unicode with only ASCII chars
        compute_webhook_validation_key(str('str app key'))
        compute_webhook_validation_key(u'unicode app key')

        # Non-ASCII chars! (really this should never come up because app keys
        # should only contain digits and a-f as they are hex strings)
        compute_webhook_validation_key(u'ʎǝʞ ddɐ ǝpoɔᴉun')
