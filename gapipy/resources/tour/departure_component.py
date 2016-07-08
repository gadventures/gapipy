from __future__ import unicode_literals

from ...models.base import BaseModel
from ...utils import get_resource_class_from_resource_name
from ..base import Resource


class AssociatedDossier(BaseModel):
    _as_is_fields = ["type"]
    _model_fields = [
        ("dossier", object),
    ]

    def _set_model_field(self, field, value):
        resource_cls = get_resource_class_from_resource_name(self.type)
        stub = resource_cls(value, client=self._client, stub=True)
        setattr(self, field, stub)


class DepartureComponent(Resource):
    _resource_name = 'departure_components'
    _is_listable = True
    _is_parent_resource = False

    _as_is_fields = [
        "id", "href", "name", "code", "type", "flags",
    ]

    _date_fields = ["start_date"]
    _date_time_fields_local = ["date_created", "date_last_modified"]

    _model_fields = [
        ("associated_dossier", AssociatedDossier),
    ]

    _resource_fields = [
        ('departure', 'Departure'),
    ]
