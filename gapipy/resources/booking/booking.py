# Python 2 and 3
from __future__ import unicode_literals

from gapipy.resources.base import Resource

from .agency_chain import AgencyChain
from .checkin import Checkin
from .customer import Customer
from .document import Invoice, Document
from .override import Override
from .requirement import RequirementSet
from .service import Service
from .transaction import Payment, Refund


class Booking(Resource):
    _resource_name = 'bookings'
    _is_parent_resource = True

    _as_is_fields = ['id', 'href', 'external_id', 'currency']
    _price_fields = [
        'amount_owing',
        'amount_paid',
        'amount_pending',
        'commission',
        'tax_on_commission',
    ]
    _date_fields = [
        'date_closed', 'date_of_first_travel', 'date_of_last_travel',
        'balance_due_date',
    ]
    _date_time_fields_utc = ['date_created', ]
    _resource_fields = [
        ('agency', 'Agency'),
        ('agency_chain', AgencyChain),
        ('agent', 'Agent'),
        ('associated_agency', 'Agency'),
        ('booking_company', 'BookingCompany')
    ]

    @property
    def _resource_collection_fields(self):
        return [
            ('checkins', Checkin),
            ('customers', Customer),
            ('documents', Document),
            ('invoices', Invoice),
            ('overrides', Override),
            ('payments', Payment),
            ('refunds', Refund),
            ('requirements', RequirementSet),
            ('services', Service),
        ]

    @property
    def _model_collection_fields(self):
        return [
            ('linked_bookings', Booking),
        ]
