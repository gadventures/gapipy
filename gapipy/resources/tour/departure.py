# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gapipy.models import AddOn
from gapipy.models import Address
from gapipy.models import DepartureRoom
from gapipy.models import PP2aPrice
from gapipy.models.base import BaseModel
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.product import Product

from .departure_component import DepartureComponent
from .tour_dossier import TourDossier


class DepartureRelationship(BaseModel):
    _as_is_fields = [
        "type",
        "sub_type",
    ]
    _resource_fields = [
        ("departure", "Departure"),
    ]


class LocalPayment(BaseModel):
    _as_is_fields = [
        "amount",
        "currency",
        "label",
    ]


class TravelReadyPolicy(BaseModel):
    _as_is_fields = [
        "code",
        "name",
    ]


class Departure(Product):

    _resource_name = "departures"

    _is_listable = True

    _is_parent_resource = True

    _as_is_fields = [
        "availability",
        "flags",
        "href",
        "id",
        "name",
        "nearest_finish_airport",
        "nearest_start_airport",
        "product_line",
        "program",
        "requirements",
        "sku",
    ]

    _date_fields = [
        "finish_date",
        "start_date",
    ]

    _date_time_fields_utc = [
        "date_cancelled",
        "date_created",
        "date_last_modified",
    ]

    _date_time_fields_local = [
        "earliest_departure_time",
        "latest_arrival_time",
    ]

    _resource_fields = [
        ("tour_dossier", TourDossier),
        ("tour", "Tour"),
    ]

    _resource_collection_fields = [
        ("components", DepartureComponent),
    ]

    _model_fields = [
        ("finish_address", Address),
        ("start_address", Address),
        ("travel_ready_policy", TravelReadyPolicy),
    ]

    _model_collection_fields = [
        ("addons", AddOn),
        ("booking_companies", BookingCompany),
        ("local_payments", LocalPayment),
        ("lowest_pp2a_prices", PP2aPrice),
        ("relationships", DepartureRelationship),
        ("rooms", DepartureRoom),
        ("structured_itineraries", "Itinerary"),
    ]
