# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource
from ..tour.image import Image
from ..tour.tour_category import TourCategoryList
from ..tour.video import Video
from .details import DossierDetail, DossierDetailsMixin
from .dossier_features import DossierFeature


class TransportDossier(Resource, DossierDetailsMixin):
    _resource_name = 'transport_dossiers'

    _as_is_fields = [
        'id',
        'href',
        'type',
        'capacity',
        'dossier_segment',
        'flags',
        'name',
        'private',
        'publish_state',
    ]

    _model_collection_fields = [
        ('categories', TourCategoryList),
        ('details', DossierDetail),
        ('features', DossierFeature),
        ('images', Image),
        ('videos', Video),
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']
