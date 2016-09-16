from __future__ import unicode_literals

from ..base import Resource
from .details import DossierDetail, DossierDetailsMixin


class AccommodationDossier(Resource, DossierDetailsMixin):
    _resource_name = 'accommodation_dossiers'

    _as_is_fields = [
        'id', 'href', 'name',
        'type',
        'website',
        'property_type',
        'address',
        'features',
        'emails',
        'phone_numbers',
        'rooms',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    _resource_fields = [
        ('location', 'Place'),
        ('primary_country', 'Country'),
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
    ]
