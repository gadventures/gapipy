# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource
from .details import DossierDetail, DossierDetailsMixin
from ..tour.video import Video
from ..tour.image import Image


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
        'publish_state',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    _resource_fields = [
        ('location', 'Place'),
        ('primary_country', 'Country'),
        ('dossier_segment', 'DossierSegment'),
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
        ('images', Image),
        ('videos', Video),
    ]
