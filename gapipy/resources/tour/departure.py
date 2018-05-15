# Python 2 and 3
from __future__ import unicode_literals

from gapipy.models import AddOn, Address, DepartureRoom, PP2aPrice
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.product import Product

from .tour_dossier import TourDossier
from .departure_component import DepartureComponent


class Departure(Product):

    _resource_name = 'departures'

    _is_listable = True

    _is_parent_resource = True

    _as_is_fields = [
        'id',
        'href',
        'name',
        'availability',
        'flags',
        'nearest_start_airport',
        'nearest_finish_airport',
        'product_line',
        'sku',
        'requirements',
    ]
    _date_fields = [
        'start_date',
        'finish_date',
    ]
    _date_time_fields_utc = [
        'date_created',
        'date_last_modified',
        'date_cancelled',
    ]
    _date_time_fields_local = [
        'latest_arrival_time',
        'earliest_departure_time',
    ]
    _resource_fields = [
        ('tour', 'Tour'),
        ('tour_dossier', TourDossier),
    ]
    _resource_collection_fields = [
        ('components', DepartureComponent),
    ]
    _model_fields = [
        ('start_address', Address),
        ('finish_address', Address),
    ]
    _model_collection_fields = [
        ('addons', AddOn),
        ('booking_companies', BookingCompany),
        ('lowest_pp2a_prices', PP2aPrice),
        ('rooms', DepartureRoom),
        ('structured_itineraries', 'Itinerary'),
    ]
