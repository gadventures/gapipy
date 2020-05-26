# Python 2 and 3
from __future__ import unicode_literals

from gapipy.models import Address
from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource

from ..geo import Nationality


class MedicalDetail(BaseModel):
    _as_is_fields = ['type', 'value']


class MembershipProgram(BaseModel):
    _as_is_fields = ['code', 'label', 'value']


class Customer(Resource):
    _resource_name = 'customers'
    _is_listable = False
    _is_parent_resource = True

    _as_is_fields = [
        'account_email',
        'emergency_contacts',
        'gender',
        'href',
        'id',
        'meal_notes',
        'meal_preference',
        'medical_notes',
        'name',
        'passport',
        'phone_numbers',
        'place_of_birth',
    ]

    _date_fields = ['date_of_birth', ]

    _resource_fields = [
        ('nationality', Nationality),
    ]

    _model_fields = [
        ('address', Address),
    ]

    _model_collection_fields = [
        ('medical_details', MedicalDetail),
        ('membership_programs', MembershipProgram),
    ]

    @property
    def _resource_collection_fields(self):
        from .booking import Booking
        return [
            ('bookings', Booking),
        ]
