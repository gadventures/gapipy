# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource

from .transaction import Payment, Refund
from .document import Invoice, Document
from .override import Override
from .service import Service
from gapipy.resources.checkin import Checkin


class Booking(Resource):
    _resource_name = 'bookings'
    _is_parent_resource = True

    _as_is_fields = ['id', 'href', 'external_id', 'currency']
    _price_fields = [
        'amount_paid', 'amount_owing', 'commission', 'tax_on_commission',
    ]
    _date_fields = [
        'date_closed', 'date_of_first_travel', 'date_of_last_travel',
        'balance_due_date',
    ]
    _date_time_fields_utc = ['date_created', ]
    _resource_fields = [
        ('agent', 'Agent'),
        ('associated_agency', 'Agency'),
    ]

    @property
    def _resource_collection_fields(self):
        return [
            ('services', Service),
            ('invoices', Invoice),
            ('payments', Payment),
            ('refunds', Refund),
            ('documents', Document),
            ('overrides', Override),
            ('checkins', Checkin),
        ]
