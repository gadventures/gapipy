# Python 2 and 3
from __future__ import unicode_literals

from gapipy.models import PriceBand
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.dossier import ActivityDossier
from gapipy.resources.product import Product


class Activity(Product):

    _resource_name = 'activities'

    _is_listable = False

    _as_is_fields = [
        'id',
        'href',
        'availability',
        'name',
        'description',
        'product_line',
        'sku',
        'type',
        'sub_type',
        'requirements',
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
        ('booking_companies', BookingCompany),
        ('price_bands', PriceBand),
    ]
    _resource_fields = [
        ('activity_dossier', ActivityDossier),
    ]
