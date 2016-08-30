from __future__ import unicode_literals

from ..base import Resource


class Customer(Resource):
    _resource_name = 'customers'
    _is_listable = False
    _is_parent_resource = True

    _as_is_fields = [
        'id', 'href', 'place_of_birth', 'meal_preference', 'meal_notes',
        'emergency_contacts', 'medical_notes', 'phone_numbers',
        'account_email', 'name', 'passport', 'address', 'nationality',
        'gender',
    ]

    _date_fields = ['date_of_birth', ]

    @property
    def _resource_collection_fields(self):
        from .booking import Booking
        return [
            ('bookings', Booking),
        ]
