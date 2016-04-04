# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from functools import partial, wraps
from importlib import import_module


def get_resource_class_from_class_name(name):
    resource_module = import_module('gapipy.resources')
    return getattr(resource_module, name)


def get_resource_class_from_resource_name(name):
    mapping = {resource._resource_name: resource
               for resource in get_available_resource_classes()}
    return mapping[name]


def get_available_resource_classes():
    from .resources import available_resources
    resource_module = import_module('gapipy.resources')
    return [getattr(resource_module, r) for r in available_resources]


def dict_to_model(class_name=None):
    """
    Wrapper to be used within resource definitions for objects you'd like to be
    dot-accessible without explicitly defining model fields for any nested data.

    You should use this with ``_model_fields`` or ``_model_collection_fields``,
    like so::

        _model_collection_fields = [
            ('phone_numbers', dict_to_model('Phone Numbers')),
        ]

    The optional ``class_name`` simply improves readability of the object
    within a debug environment.
    """
    from .models.base import DictToModel
    return partial(DictToModel, class_name=class_name)


def is_free(amount):
    """
    Explit zero amounts are interpreted as Free!
    """
    return (
        amount == 0 or
        amount == 0.00 or
        amount == '0' or
        amount == '0.00'
    )


def humanize_amount(amount, force_decimal=False):
    """
    Takes an `amount` (float) and removes any unnecessary decimals,
    or adds them if there is any partial amount.

    TODO: Internationalization support
    """
    if is_free(amount):
        return 'Free'

    amount = float(amount)
    if amount % 1 or force_decimal:
        return '%.2f' % amount
    return '%.0f' % amount


def humanize_price(amount_min, amount_max, currency):
    """
    Format a single price or price range for display.
    """
    # No price, nothing to display
    if amount_min is None:
        return ''

    # Price Range
    if amount_max:
        human_min = humanize_amount(amount_min)
        # If the miniumum has a decimal, then we want the max
        # to also have decimal places.
        force_decimal = '.' in human_min
        return '{}-{}{}'.format(
            human_min,
            humanize_amount(amount_max, force_decimal=force_decimal),
            currency,
        )
    # Single Price
    return '{}{}'.format(
        humanize_amount(amount_min),
        currency if not is_free(amount_min) else '',
    )


def humanize_time(hours):
    """
    Make a friendly duration label for display. e.g. Takes a value
    like 2.75 and returns 2h45m.
    """
    if not hours:
        return ''
    # TODO: Why are durations strings in our API?
    hours = float(hours)
    minutes = int(hours % 1 * 60)
    whole_hrs = int(hours)
    if minutes and whole_hrs:
        return '{}h{}m'.format(whole_hrs, minutes)
    elif minutes:
        return '{}m'.format(minutes)
    elif whole_hrs:
        return '{}h'.format(whole_hrs)


def location_label(start, end):
    """
    `start` and `end` are to locations that have a name property
    """
    if not start:
        return ''

    if end and end.name != start.name:
        return '{} – {}'.format(
            start.name,
            end.name,
        )
    return start.name


def duration_label(min_hr, max_hr):
    """
    Helper to output a friendly duration single value or range.
    """
    if not min_hr:
        return ''
    if max_hr:
        return '{}-{}'.format(humanize_time(min_hr), humanize_time(max_hr))
    return humanize_time(min_hr)


class LocationLabelMixin(object):
    """
    Mixin for resources with `start_location` and `end_location` fields.
    Formats a friendly label like Toronto - Monteal, or just a single
    location if both start and end are the same.
    """
    @property
    def location_label(self):
        return location_label(self.start_location, self.end_location)


class DurationLabelMixin(object):
    """
    Mixin for resources with a duration dict to format a human friendly
    single or ranged duration.
    """
    @property
    def duration_label(self):
        if not self.duration:
            return ''
        return self.duration.label


def enforce_string_type(func):
    """Force the output of __repr__ to be of the proper string type, depending
    of the Python version.

    In Python 2, the output of `__repr__` must be a byte string, while in
    Python 3, it must be unicode. Since the string representation of many G API
    resources contain words in non-English languages, they can contain
    characters outside of the ASCII range, which raises a UnicodeEncodeError
    when it is implictly coerced to the default encoding by Python.

    The way we ensure the return of a proper string type in Python 2 is by
    encoding the output to UTF-8. This might not be adequate in all use cases
    of gapipy, but this is what Django does in its codebase, and this seems
    like a good default.
    """
    if sys.version_info.major > 2:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).encode('utf-8')

    return wrapper
