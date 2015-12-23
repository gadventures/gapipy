from __future__ import unicode_literals

from ...models import Address, AddOn, DepartureRoom, PP2aPrice

from ..base import Product
from .tour_dossier import TourDossier
from .departure_component import DepartureComponent


class Departure(Product):

    _resource_name = 'departures'
    _is_listable = True
    _is_parent_resource = True

    _as_is_fields = [
        'id', 'href', 'name', 'availability', 'flags', 'nearest_start_airport',
        'nearest_finish_airport', 'product_line', 'sku', 'requirements',
    ]
    _date_fields = ['start_date', 'finish_date']
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _date_time_fields_local = ['latest_arrival_time', 'earliest_departure_time']
    _resource_fields = [('tour', 'Tour'), ('tour_dossier', TourDossier)]
    _resource_collection_fields = [
        ('components', DepartureComponent),
    ]
    _model_fields = [('start_address', Address), ('finish_address', Address)]
    _model_collection_fields = [
        ('addons', AddOn),
        ('rooms', DepartureRoom),
        ('lowest_pp2a_prices', PP2aPrice),
    ]
    _deprecated_fields = ['add_ons']
