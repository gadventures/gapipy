from __future__ import unicode_literals

from ...models import Address
from ...models import AgencyDocument
from ...models.base import BaseModel
from .agency_chain import AgencyChain

from ..base import Resource
from ..tour import Promotion


class AgencyEmail(BaseModel):
    _as_is_fields = ['type', 'address']


class Agency(Resource):
    _resource_name = 'agencies'
    _is_listable = False
    _is_parent_resource = True

    _as_is_fields = ['id', 'href', 'name', 'booking_currencies', 'latitude', 'longitude', 'transactional_email']
    _date_time_fields_local = ['date_created']
    _model_fields = [('address', Address)]
    _resource_fields = [('agency_chain', AgencyChain)]
    _model_collection_fields = [
        ('documents', AgencyDocument),
        ('emails', AgencyEmail),
    ]
    _resource_collection_fields = [
        ('bookings', 'Booking'),
        ('agents', 'Agent'),
        ('promotions', Promotion),
    ]
