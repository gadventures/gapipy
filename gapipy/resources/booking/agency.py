# Python 2 and 3
from __future__ import unicode_literals

from gapipy.models import Address, AgencyDocument
from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.tour import Promotion

from .agency_chain import AgencyChain


class AgencyEmail(BaseModel):
    _as_is_fields = ['type', 'address']


class Agency(Resource):
    _resource_name = 'agencies'
    _is_listable = False
    _is_parent_resource = True

    _as_is_fields = [
        'id',
        'href',
        'name',
        'booking_currencies',
        'latitude',
        'longitude',
        'transactional_email',
        'communication_preferences',
        'override_agency_secondary',
        'passenger_notifications',
        'agent_notifications',
        'preferred_display_name',
    ]
    _date_time_fields_local = [
        'date_created',
    ]
    _model_fields = [
        ('address', Address),
    ]
    _resource_fields = [
        ('agency_chain', AgencyChain),
    ]
    _model_collection_fields = [
        ('agency_chains', 'AgencyChain'),
        ('booking_companies', BookingCompany),
        ('documents', AgencyDocument),
        ('emails', AgencyEmail),
    ]
    _resource_collection_fields = [
        ('agents', 'Agent'),
        ('promotions', Promotion),
    ]
