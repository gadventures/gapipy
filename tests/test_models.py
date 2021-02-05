# -*- coding: utf-8 -*-
# Python 2 and 3
from __future__ import unicode_literals

from unittest import TestCase

import datetime

from gapipy.models.valid_during_range import ValidDuringRange


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
