# Python 2 and 3
from __future__ import unicode_literals

from gapipy.models import Address, AccommodationRoom
from gapipy.utils import enforce_string_type
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.dossier import AccommodationDossier
from gapipy.resources.product import Product


class Accommodation(Product):

    _resource_name = 'accommodations'

    _as_is_fields = [
        'id',
        'href',
        'name',
        'product_line',
        'sku',
        'type',
        'sub_type',
        'phone_numbers',
    ]
    _date_time_fields_utc = [
        'date_created',
        'date_last_modified',
    ]
    _model_fields = [
        ('address', Address),
    ]
    _model_collection_fields = [
        ('booking_companies', BookingCompany),
        ('rooms', AccommodationRoom),
    ]
    _resource_fields = [
        ('accommodation_dossier', AccommodationDossier),
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
