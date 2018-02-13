# Python 2 and 3
from __future__ import unicode_literals

from gapipy.resources.base import Resource
from gapipy.resources.booking_company import BookingCompany


class AgencyChain(Resource):

    _resource_name = 'agency_chains'

    _as_is_fields = [
        'id',
        'href',
        'name',
        'flags',
        'communication_preferences',
        'payment_options',
        'agencies',
        'passenger_notifications',
        'agent_notifications',
    ]
    _date_time_fields_local = [
        'date_created',
    ]
    _resource_fields = [
        ('booking_company', BookingCompany),
    ]
