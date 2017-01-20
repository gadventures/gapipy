# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource, BaseModel


class MedicalDetail(BaseModel):
    _as_is_fields = ['type', 'value']


class Customer(Resource):
    _resource_name = 'customers'
    _is_listable = False
    _is_parent_resource = True

    _as_is_fields = [
        'account_email',
        'address',
        'emergency_contacts',
        'gender',
        'href',
        'id',
        'meal_notes',
        'meal_preference',
        'medical_notes',
        'name',
        'nationality',
        'passport',
        'phone_numbers',
        'place_of_birth',
    ]

    _date_fields = ['date_of_birth', ]

    _model_collection_fields = [
        ('medical_details', MedicalDetail),
    ]

    @property
    def _resource_collection_fields(self):
        from .booking import Booking
        return [
            ('bookings', Booking),
        ]
