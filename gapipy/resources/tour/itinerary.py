from __future__ import unicode_literals

from ..base import Resource
from ...models.base import BaseModel


class ItineraryComponent(BaseModel):
    _as_is_fields = [
        'type', 'summary', 'description', 'instructions', 'duration',
        'distance_km', 'start_time', 'end_time', 'time_period', 'is_overnight',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
        ('activity_dossier', 'ActivityDossier'),
        ('transport_dossier', 'TransportDossier'),
    ]

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.type)


class ItineraryDay(BaseModel):
    _as_is_fields = [
        'id', 'day', 'summary', 'description', 'instructions', 'meals',
        'optional_activities',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
    ]
    _model_collection_fields = [
        ('components', ItineraryComponent),
    ]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.day)


class Itinerary(Resource):

    _resource_name = 'itineraries'

    _as_is_fields = [
        'id', 'href', 'duration', 'meals_included', 'meals_budget',
        'packing_lists', 'images',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
    ]
    _model_collection_fields = [
        ('days', ItineraryDay),
    ]
