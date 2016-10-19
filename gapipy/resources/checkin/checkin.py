from __future__ import unicode_literals

from ..base import Resource

class Checkin(Resource):
    _resource_name = 'checkins'
    _is_listable = True

    _as_is_fields = ['id']
    _date_fields = ['expires']
    _resource_fields = [
        ('booking', 'Booking'),
        ('customer', 'Customer'),
    ]
