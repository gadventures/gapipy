# -*- coding: utf-8 -*-
# Python 2 and 3
from __future__ import unicode_literals

import datetime

from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.tour.image import Image, MAP_TYPE
from gapipy.utils import (
    DurationLabelMixin,
    LocationLabelMixin,
    duration_label,
    enforce_string_type,
)


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
        'description',
        'distance_km',
        'end_time',
        'instructions',
        'is_overnight',
        'start_time',
        'summary',
        'time_period',
        'type',
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
        'id',
        'day',
        'label',
        'summary',
        'description',
        'instructions',
        'meals',
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
    _date_fields = [
        'end_date',
        'start_date',
    ]

    def is_expired(self):
        return not self.is_valid_during_range(datetime.date.today(), None)

    def is_valid_today(self):
        return self.is_valid_on_date(datetime.date.today())

    def is_valid_during_range(self, start_date, end_date):
        if start_date and not end_date:
            return self.is_valid_on_or_after_date(start_date)

        if not start_date and end_date:
            return self.is_valid_on_or_before_date(end_date)

        if not start_date and not end_date:
            return self.is_valid_sometime()

        if start_date == end_date:
            return self.is_valid_on_date(start_date)

        # start_date and end_date are both not None and not equal
        return (
            start_date <= end_date
        ) and (
            self.is_valid_sometime()
        ) and all([
            self.start_date is None or self.start_date <= end_date,
            self.end_date is None or self.end_date >= start_date,
        ])

    def is_valid_on_or_after_date(self, date):
        return (
            self.end_date is None
        ) or (
            self.start_date is None and
            self.end_date >= date
        ) or (
            self.start_date is not None and
            self.start_date <= self.end_date and
            self.end_date >= date
        )

    def is_valid_on_or_before_date(self, date):
        return (
            self.start_date is None
        ) or (
            self.end_date is None and
            self.start_date <= date
        ) or (
            self.end_date is not None and
            self.start_date <= self.end_date and
            self.start_date <= date
        )

    def is_valid_on_date(self, date):
        return all([
            self.start_date is None or self.start_date <= date,
            self.end_date is None or self.end_date >= date,
        ])

    def is_valid_sometime(self):
        return (
            self.start_date is None or
            self.end_date is None or
            self.start_date <= self.end_date
        )

    @enforce_string_type
    def __repr__(self):
        return '<{} ({} - {})>'.format(self.__class__.__name__, self.start_date, self.end_date)


class DetailType(BaseModel):
    _as_is_fields = [
        'id',
        'code',
        'name',
    ]

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
        'id',
        'type',
        'image',
        'video_thumb',
        'videos',
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.type)


class ItineraryHighlights(Resource):
    _resource_name = 'itinerary_highlights'

    _as_is_fields = [
        'id',
        'name',
        'description',
        'media',
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)


class Itinerary(Resource):
    _resource_name = 'itineraries'

    _is_parent_resource = True

    _as_is_fields = [
        'id',
        'href',
        'name',
        'flags',
        'duration',
        'meals_included',
        'meals_budget',
        'packing_lists',
        'site_links',
        'variation_id',
    ]
    _resource_fields = [
        ('end_location', 'Place'),
        ('start_location', 'Place'),
        ('tour_dossier', 'TourDossier'),
    ]
    _model_collection_fields = [
        ('booking_companies', BookingCompany),
        ('days', ItineraryDay),
        ('details', Detail),
        ('images', Image),
        ('valid_during_ranges', ValidDuringRange),
        ('variations', 'Itinerary'),
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
        Returns the URL of this itinerary's map image (or None if no map image
        is found, see get_map_image())
        """
        image = self.get_map_image()
        if not image or not getattr(image, 'file', None):
            return None
        return image.file.url

    def is_expired(self):
        return all([
            vrange.is_expired()
            for vrange in self.valid_during_ranges
        ])

    def is_valid_today(self):
        return any([
            vrange.is_valid_today()
            for vrange in self.valid_during_ranges
        ])

    def is_valid_during_range(self, start_date, end_date):
        return any([
            vrange.is_valid_during_range(start_date, end_date)
            for vrange in self.valid_during_ranges
        ])

    def is_valid_on_or_after_date(self, date):
        return any([
            vrange.is_valid_on_or_after_date(date)
            for vrange in self.valid_during_ranges
        ])

    def is_valid_on_or_before_date(self, date):
        return any([
            vrange.is_valid_on_or_before_date(date)
            for vrange in self.valid_during_ranges
        ])

    def is_valid_on_date(self, date):
        return any([
            vrange.is_valid_on_date(date)
            for vrange in self.valid_during_ranges
        ])

    def is_valid_sometime(self):
        return any([
            vrange.is_valid_sometime()
            for vrange in self.valid_during_ranges
        ])
