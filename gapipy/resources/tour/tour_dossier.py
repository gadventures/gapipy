# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gapipy.constants import IMAGE_TYPE_BANNER
from gapipy.constants import IMAGE_TYPE_MAP
from gapipy.models import AdvertisedDeparture, ValidDuringRange
from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource
from gapipy.resources.booking_company import BookingCompany


class TourDossierRelationship(BaseModel):
    _as_is_fields = [
        'type',
        'sub_type',
    ]
    _resource_fields = [
        ('tour_dossier', 'TourDossier'),
    ]
    _model_collection_fields = [
        ('valid_during_ranges', ValidDuringRange),
    ]


class TourDossier(Resource):

    _resource_name = 'tour_dossiers'
    _is_parent_resource = True

    _as_is_fields = [
        'id',
        'href',
        'categories',
        'description',
        'details',
        'product_line',
        'geography',
        'images',
        'name',
        'site_links',
        'slug',
    ]

    _date_fields = [
        'departures_start_date',
        'departures_end_date',
    ]

    _resource_fields = [
        ('tour', 'Tour'),
    ]

    _resource_collection_fields = [
        ('departures', 'Departure'),
    ]

    _model_collection_fields = [
        ('advertised_departures', AdvertisedDeparture),
        ('booking_companies', BookingCompany),
        ('relationships', TourDossierRelationship),
        ('structured_itineraries', 'Itinerary'),
    ]

    def _get_image_url(self, image_type):
        for image in self.images:
            if image['type'] == image_type:
                return image['image_href']
        return None

    def get_map_url(self):
        return self._get_image_url(IMAGE_TYPE_MAP)

    def get_banner_url(self):
        return self._get_image_url(IMAGE_TYPE_BANNER)

    def get_visited_countries(self):
        return [country['name'] for country in self.geography['visited_countries']]

    def get_trip_detail(self, label):
        for detail in self.details:
            if detail['detail_type']['label'] == label:
                return detail['body']
        return None

    def get_category_name(self, label):
        for category in self.categories:
            if category['category_type']['label'] == label:
                return category['name']
        return None
