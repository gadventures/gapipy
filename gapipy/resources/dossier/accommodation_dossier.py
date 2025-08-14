# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource
from ..dossier.dossier_features import DossierFeature
from ..tour.image import Image
from ..tour.tour_category import TourCategoryList
from ..tour.video import Video
from .details import DossierDetail, DossierDetailsMixin


class AccommodationDossier(Resource, DossierDetailsMixin):
    _resource_name = 'accommodation_dossiers'
    _is_listable = True

    _as_is_fields = [
        'id',
        'href',
        'type',
        'address',
        'emails',
        'flags',
        'name',
        'phone_numbers',
        'property_type',
        'publish_state',
        'rooms',
        'service_code',
        'service_time',
        'show_on_reservation_sheet',
        'suggested_dossiers',  # FIXME: these are typed references to other *_dossiers
        'website',
    ]

    _date_time_fields_local = [
        'date_created',
        'date_last_modified',
    ]

    _resource_fields = [
        ('location', 'Place'),
        ('primary_country', 'Country'),
        ('dossier_segment', 'DossierSegment'),
    ]

    _model_collection_fields = [
        ('categories', TourCategoryList),
        ('details', DossierDetail),
        ('features', DossierFeature),
        ('images', Image),
        ('videos', Video),
        ('visited_cities', 'Place'),
        ('visited_countries', 'Country'),
    ]
