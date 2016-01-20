from __future__ import unicode_literals

from ...query import Query
from ...utils import get_resource_class_from_class_name

from ..base import Resource
from ...models import AdvertisedDeparture


BRIEF_ITINERARY_TYPE = 'SUMMARY'
DETAILED_ITINERARY_TYPE = 'DETAILED'
MAP_IMAGE_TYPE = 'MAP'
BANNER_IMAGE_TYPE = 'BANNER'


class TourDossier(Resource):

    _resource_name = 'tour_dossiers'

    _as_is_fields = [
        'id', 'href', 'categories', 'description', 'details', 'product_line',
        'geography', 'images', 'itineraries', 'name', 'site_links',
    ]
    _date_fields = ['departures_start_date', 'departures_end_date']
    _resource_fields = [('tour', 'Tour')]
    _resource_collection_fields = [
        ('departures', 'Departure'),
    ]
    _model_collection_fields = [
        ('advertised_departures', AdvertisedDeparture),
        ('structured_itineraries', 'Itinerary'),
    ]

    def _set_resource_collection_field(self, field, value):
        """Overridden to ensure that the `departures` query has the right
        parent resource (i.e. the tour and not the tour dossier).
        """

        if field == 'departures':
            resource_cls = get_resource_class_from_class_name('Departure')

            # Tour dossiers always have the same id as the corresponding tour
            parent = ('tours', self.id, None)

            setattr(self, 'departures', Query(self._client, resource_cls, parent=parent, raw_data=value))
        else:
            return super(TourDossier, self)._set_resource_collection_field(field, value)

    def _get_itinerary(self, itinerary_type):
        for itin in self.itineraries:
            if itin['type'] == itinerary_type:
                return [dict(label=i['label'], body=i['body']) for i in itin['days']]

    def get_brief_itinerary(self):
        return self._get_itinerary(BRIEF_ITINERARY_TYPE)

    def get_detailed_itinerary(self):
        return self._get_itinerary(DETAILED_ITINERARY_TYPE)

    def _get_image_url(self, image_type):
        for image in self.images:
            if image['type'] == image_type:
                return image['image_href']

    def get_map_url(self):
        return self._get_image_url(MAP_IMAGE_TYPE)

    def get_banner_url(self):
        return self._get_image_url(BANNER_IMAGE_TYPE)

    def get_visited_countries(self):
        return [country['name'] for country in self.geography['visited_countries']]

    def get_trip_detail(self, label):
        for detail in self.details:
            if detail['detail_type']['label'] == label:
                return detail['body']
