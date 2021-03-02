# -*- coding: utf-8 -*-

# pylint: disable=no-member
from __future__ import unicode_literals

from gapipy.constants import IMAGE_TYPE_MAP
from gapipy.models import ValidDuringRange
from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource
from gapipy.resources.booking_company import BookingCompany
from gapipy.resources.tour.image import Image
from gapipy.utils import DurationLabelMixin
from gapipy.utils import LocationLabelMixin
from gapipy.utils import duration_label
from gapipy.utils import enforce_string_type


class RippleScore(BaseModel):
    _as_is_fields = [
        'score',
        'end_date',
        'start_date',
    ]


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
        'publish_state',
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

    _model_fields = [
        ('ripple_score', RippleScore),
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
            if image.type == IMAGE_TYPE_MAP:
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
