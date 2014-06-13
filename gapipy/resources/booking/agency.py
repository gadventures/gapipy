from __future__ import unicode_literals

from ...models import Address

from ..base import Resource
from ..tour import Promotion


class Agency(Resource):
    _resource_name = 'agencies'
    _is_listable = False
    _is_parent_resource = True

    _as_is_fields = ['id', 'href', 'name', 'booking_currencies']
    _date_time_fields_utc = ['date_created']
    _model_fields = [('address', Address)]
    _resource_collection_fields = [
        ('bookings', 'Booking'),
        ('agents', 'Agent'),
        ('promotions', Promotion),
    ]
