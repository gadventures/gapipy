# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource
from ..tour.image import Image
from ..tour.video import Video
from .details import DossierDetail


class PlaceDossier(Resource):
    _resource_name = 'place_dossiers'

    _as_is_fields = [
        'id',
        'href',
        'type',
        'flags',
        'name',
        'publish_state',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    _resource_fields = [
        ('place', 'Place')
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
        ('images', Image),
        ('videos', Video),
    ]
