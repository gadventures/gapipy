from __future__ import unicode_literals

from ..base import Resource
from .country import Country
from .feature import Feature
from .state import State
from .timezone import Timezone

from ..dossier import PlaceDossier


class Place(Resource):

    _resource_name = 'places'

    _as_is_fields = [
        'id', 'href', 'name', 'ascii_name', 'population', 'elevation',
        'latitude', 'longitude', 'bounding_box', 'alternate_names',
        'admin_divisions',
    ]
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _resource_fields = [
        ('country', Country),
        ('state', State),
        ('feature', Feature),
        ('timezone', Timezone),
    ]

    _model_fields = [
        ('place_dossier', PlaceDossier),
    ]

    _model_collection_fields = [
        ('places_of_interest', 'Place')
    ]

    def __init__(self, *args, **kwargs):
        super(Place, self).__init__(*args, **kwargs)
        self._set_admin_divisions()

    def _set_admin_divisions(self):
        """Transform the raw json list of `admin_divisions` into a list of thecd ~?
        corresponding Place (stub) instances.
        """
        if 'admin_divisions' in self._raw_data:
            raw_admin_divisions = self._raw_data['admin_divisions'] or []
            admin_divisions = [
                self.__class__(d, client=self._client, stub=True)
                for d in raw_admin_divisions
            ]
            self.admin_divisions = admin_divisions
