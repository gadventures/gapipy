# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..base import Resource
from ...models.base import BaseModel
from ...utils import duration_label, LocationLabelMixin, DurationLabelMixin


class OptionalActivity(BaseModel):
    _resource_fields = [
        ('activity_dossier', 'ActivityDossier'),
    ]

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.activity_dossier)


class Duration(BaseModel):
    _as_is_fields = [
        'min_hr', 'max_hr',
    ]

    def __repr__(self):
        return '<{}: {},{}>'.format(self.__class__.__name__, self.min_hr, self.max_hr)

    @property
    def label(self):
        return duration_label(self.min_hr, self.max_hr)


class ItineraryComponent(BaseModel, DurationLabelMixin, LocationLabelMixin):
    _as_is_fields = [
        'type',
        'summary', 'description', 'instructions',
        'distance_km', 'start_time', 'end_time', 'time_period', 'is_overnight',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
        ('activity_dossier', 'ActivityDossier'),
        ('transport_dossier', 'TransportDossier'),
    ]
    _model_fields = [
        ('duration', 'Duration'),
    ]

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.type)

    @property
    def is_free_time(self):
        return self.type == 'FREE_TIME'

    @property
    def is_activity(self):
        return self.type == 'ACTIVITY'

    @property
    def is_transport(self):
        return self.type == 'TRANSPORT'


class ItineraryDay(BaseModel):
    _as_is_fields = [
        'id', 'day', 'summary', 'description', 'instructions', 'meals',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
    ]
    _model_collection_fields = [
        ('components', ItineraryComponent),
        ('optional_activities', OptionalActivity),
    ]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.day)


class Itinerary(Resource):

    _resource_name = 'itineraries'

    _as_is_fields = [
        'id', 'href', 'name', 'duration', 'meals_included', 'meals_budget',
        'packing_lists', 'images',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
    ]
    _model_collection_fields = [
        ('days', ItineraryDay),
    ]
