# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .image import Image, MAP_TYPE
from ..base import Resource
from ...models.base import BaseModel
from ...utils import DurationLabelMixin, LocationLabelMixin, duration_label, enforce_string_type


class OptionalActivity(BaseModel):
    _resource_fields = [
        ('activity_dossier', 'ActivityDossier'),
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.activity_dossier)


class Duration(BaseModel):
    _as_is_fields = [
        'min_hr', 'max_hr',
    ]

    @enforce_string_type
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
        ('accommodation_dossier', 'AccommodationDossier'),
        ('activity_dossier', 'ActivityDossier'),
        ('transport_dossier', 'TransportDossier'),
    ]
    _model_fields = [
        ('duration', 'Duration'),
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.type)

    @property
    def is_free_time(self):
        return self.type == 'FREE_TIME'

    @property
    def is_accommodation(self):
        return self.type == 'ACCOMMODATION'

    @property
    def is_activity(self):
        return self.type == 'ACTIVITY'

    @property
    def is_transport(self):
        return self.type == 'TRANSPORT'


class ItineraryDay(BaseModel):
    _as_is_fields = [
        'id', 'day', 'label', 'summary', 'description', 'instructions', 'meals',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
    ]
    _model_collection_fields = [
        ('components', ItineraryComponent),
        ('optional_activities', OptionalActivity),
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.day)


class ValidDuringRange(BaseModel):
    _date_fields = ['start_date', 'end_date']

    @enforce_string_type
    def __repr__(self):
        return '<{} ({} - {})>'.format(self.__class__.__name__, self.start_date, self.end_date)


class DetailType(BaseModel):
    _as_is_fields = ['id', 'name', 'code']

    @enforce_string_type
    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.code)


class Detail(BaseModel):
    _as_is_fields = ['body']

    _model_fields = [
        ('type', DetailType),
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{} {}: {}>'.format(self.__class__.__name__, self.type.code, self.body[:100])


class ItineraryMedia(Resource):

    _resource_name = 'itinerary_media'

    _as_is_fields = [
        'id', 'type', 'video_thumb', 'videos', 'image',
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.type)


class ItineraryHighlights(Resource):
    _resource_name = 'itinerary_highlights'

    _as_is_fields = ['id', 'name', 'description', 'media']

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)


class Itinerary(Resource):

    _resource_name = 'itineraries'
    _is_parent_resource = True

    _as_is_fields = [
        'id', 'href', 'name', 'duration', 'meals_included', 'meals_budget',
        'packing_lists', 'variation_id',
    ]
    _resource_fields = [
        ('start_location', 'Place'),
        ('end_location', 'Place'),
        ('tour_dossier', 'TourDossier'),
    ]
    _model_collection_fields = [
        ('days', ItineraryDay),
        ('details', Detail),
        ('variations', 'Itinerary'),
        ('valid_during_ranges', ValidDuringRange),
        ('images', Image),
    ]

    _resource_collection_fields = [
        ('media', ItineraryMedia),
        ('highlights', ItineraryHighlights),
    ]

    def get_map_image(self):
        """
        Returns the first Image in our list that claims to be a map. Returns
        None if no Images are listed, or if none are marked as a map image.
        """
        for image in self.images:
            if getattr(image, 'type', None) == MAP_TYPE:
                return image
        return None

    def get_map_url(self):
        """
        Returns the URL of this itinerary's map image (or None of no map image
        is found, see get_map_image())
        """
        image = self.get_map_image()
        if not image or not getattr(image, 'file', None):
            return None
        return image.file.url
