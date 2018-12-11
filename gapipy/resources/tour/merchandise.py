# Python 2 and 3
from __future__ import unicode_literals

from gapipy.models import PriceBand
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.product import Product


class Merchandise(Product):

    _resource_name = 'merchandise'

    _is_listable = False

    _as_is_fields = [
        'id',
        'availability',
        'name',
        'product_line',
        'sku',
        'type',
        'sub_type',
        'href',
    ]
    _date_fields = [
        'start_date',
        'finish_date',
    ]
    _date_time_fields_utc = [
        'date_created',
        'date_last_modified',
    ]
    _model_collection_fields = [
        ('price_bands', PriceBand),
    ]
