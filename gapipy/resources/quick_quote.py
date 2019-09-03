# Python 2 and 3
from __future__ import unicode_literals

from .base import Resource


class QuickQuote(Resource):

    _resource_name = 'quick_quotes'

    _as_is_fields = [
        'id',
        'href',
        'opportunity_id',
        'adult_pax',
        'child_pax',
        'total_pax',
        'foc_travellers',
        'single_rooms',
        'twin_rooms',
        'triple_rooms',
        'quadruple_rooms',
        'duration',
        'has_ceo',
        'currency',
        'reporting_office',
        'pricing',
        'days',
        'base_itinerary',
        'notes',
    ]
    _date_fields = [
        'start_date',
    ]
