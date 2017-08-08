# Python 2 and 3
from __future__ import unicode_literals
import warnings

from ..base import Resource
from .departure import Departure
from .tour_dossier import TourDossier


class Tour(Resource):

    _resource_name = 'tours'
    _is_parent_resource = True

    _as_is_fields = ['id', 'href', 'product_line']
    _date_fields = ['departures_start_date', 'departures_end_date']
    _resource_fields = [('tour_dossier', TourDossier)]
    _resource_collection_fields = [('departures', Departure)]

    def __init__(self, *args, **kwargs):
        warnings.warn("""
            The `tours` resource will be deprecated in the near
            future in favour of `tour_dossiers`. Please reference
            `tour_dossiers` going forward
        """, DeprecationWarning)
        super(Tour, self).__init__(*args, **kwargs)

    def get_brief_itinerary(self):
        return self.tour_dossier.get_brief_itinerary()

    def get_detailed_itinerary(self):
        return self.tour_dossier.get_detailed_itinerary()

    def get_map_url(self):
        return self.tour_dossier.get_map_url()

    def get_banner_url(self):
        return self.tour_dossier.get_banner_url()

    def get_visited_countries(self):
        return self.tour_dossier.get_visited_countries()

    def get_trip_detail(self, label):
        return self.tour_dossier.get_trip_detail(label)
