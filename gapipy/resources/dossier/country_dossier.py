# Python 2 and 3
from __future__ import unicode_literals

from gapipy.resources.base import Resource
from gapipy.models.base import BaseModel

from .details import DossierDetail
from .dossier_features import DossierFeature


class MealBudget(BaseModel):
    _as_is_fields = [
        'id',
        'quality',
        'meal_type',
        'amount',
    ]


class CountryDossier(Resource):
    _resource_name = 'country_dossiers'

    _as_is_fields = [
        'id',
        'href',
        'type',
        'flags',
        'name',
        'publish_state',
    ]

    _date_time_fields_local = [
        'date_created',
        'date_last_modified',
    ]

    _resource_fields = [
        ('country', 'Country'),
        ('dossier_segment', 'DossierSegment'),
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
        ('features', DossierFeature),
        ('meal_budgets', MealBudget),
    ]
