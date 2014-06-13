from __future__ import unicode_literals

from ..base import Resource


class BaseTransaction(Resource):
    _is_listable = False

    _as_is_fields = ['id', 'href', 'status', 'transaction_type', 'error']
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _price_fields = ['amount']
    _resource_fields = [
        ('booking', 'Booking'),
    ]


class Refund(BaseTransaction):
    _resource_name = 'refunds'
    _price_fields = ['amount', 'commission']


class Payment(BaseTransaction):
    _resource_name = 'payments'
