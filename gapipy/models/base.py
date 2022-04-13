import datetime
import sys
from collections import namedtuple
from copy import deepcopy
from decimal import Decimal

from gapipy.constants import DATE_FORMAT
from gapipy.constants import DATE_TIME_LOCAL_FORMAT
from gapipy.constants import DATE_TIME_UTC_FORMAT
from gapipy.query import Query
from gapipy.utils import get_resource_class_from_class_name
from gapipy.utils import get_resource_class_from_resource_name


# _Parent is a 3-Tuple that is used to store the based URI of a Resource, the
# ID, and Variation ID if it has one
_Parent = namedtuple("_Parent", ["uri", "id", "variation_id"])

class BaseModel(object):
    """
    A base for any Resource or model type. The difference being a Resource
    points to a specific API resource while a model type might have a reference
    to a resource but is mostly nested type that is complex and has attributes
    adjusted for it.
    """
    _as_is_fields = []
    _date_fields = []
    _date_time_fields_utc = []
    _date_time_fields_local = []
    _model_fields = []
    _model_collection_fields = []
    _price_fields = []
    _resource_fields = []
    _resource_collection_fields = []
    _deprecated_fields = []

    def __init__(self, data, client):
        self._client = client
        self._raw_data = deepcopy(data)
        self._fill_fields(data)

    def _fill_fields(self, data):
        self._raw_data = deepcopy(data)
        first = lambda l: [pair[0] for pair in l]

        # Initially we populate base fields, as model/resource fields may rely
        # on these to be present.
        remaining_data = {}

        if not isinstance(data, dict):
            raise AttributeError(
                "Unable to populate resource. Failed at data point: {}".format(data)
            )

        for field, value in list(data.items()):
            if field in self._as_is_fields:
                self._set_as_is_field(field, value)
            elif field in self._date_fields:
                self._set_date_field(field, value)
            elif field in self._date_time_fields_local:
                self._set_date_time_field_local(field, value)
            elif field in self._date_time_fields_utc:
                self._set_date_time_field_utc(field, value)
            elif field in self._price_fields:
                self._set_price_field(field, value)
            else:
                remaining_data[field] = value

        # Populate resource/model fields.
        # list(dict.items()) inefficient on Python 2
        for field, value in list(remaining_data.items()):
            if field in first(self._model_fields):
                self._set_model_field(field, value)
            elif field in first(self._model_collection_fields):
                self._set_model_collection_field(field, value)
            elif field in first(self._resource_fields):
                self._set_resource_field(field, value)
            elif field in first(self._resource_collection_fields):
                self._set_resource_collection_field(field, value)

    def _set_as_is_field(self, field, value):
        setattr(self, field, value)

    def _set_date_field(self, field, value):
        if value:
            value = datetime.datetime.strptime(value, DATE_FORMAT).date()
        setattr(self, field, value)

    def _set_date_time_field_local(self, field, value):
        if value:
            value = datetime.datetime.strptime(value, DATE_TIME_LOCAL_FORMAT)
        setattr(self, field, value)

    def _set_date_time_field_utc(self, field, value):
        if value:
            value = datetime.datetime.strptime(value, DATE_TIME_UTC_FORMAT)
        setattr(self, field, value)

    def _set_price_field(self, field, value):
        if value:
            value = Decimal(value)
        setattr(self, field, value)

    def _model_cls(self, field):
        # Find what model class this field is in reference to by plucking it
        # from the set of all fields that allow this type of definition.
        fields = (self._model_fields
                  + self._model_collection_fields
                  + self._resource_fields
                  + self._resource_collection_fields)

        model_cls = [cls for f, cls in fields if f == field][0]

        # FIXME: This will not work for the model_*_fields.

        # Python 2 has basestring, Python 3 str
        str_or_base = False
        if sys.version_info.major < 3:
            # Python 2
            if isinstance(model_cls, basestring):
                str_or_base = True
        else:
            # Python 3
            if isinstance(model_cls, str):
                str_or_base = True
        if str_or_base:
            model_cls = get_resource_class_from_class_name(model_cls)
        return model_cls

    def _set_model_field(self, field, value):
        if value is None:
            setattr(self, field, None)
        else:
            setattr(self, field, self._model_cls(field)(value, client=self._client))

    def _set_model_collection_field(self, field, value):
        from gapipy.resources.base import Resource

        model_cls = self._model_cls(field)

        # If `model_cls` can be of three type: a Resource, a BaseModel that
        # isn't a Resource. If it is a Resource, then we pass in the `stub` kwarg.
        #
        # "if Resource do this else do that",
        # since `issubclass` only accepts classes as argument.
        if issubclass(model_cls, Resource):
            items = [model_cls(m, client=self._client, stub=True) for m in value]
        else:
            items = [model_cls(m, client=self._client) for m in value]

        setattr(self, field, items)

    def _set_resource_field(self, field, value):
        if value is None:
            setattr(self, field, None)
        else:
            setattr(self, field, self._model_cls(field)(value, client=self._client, stub=True))

    def _parent(self):
        if getattr(self, "_is_parent_resource", False):
            # FIXME: stop hard-coding variation_id all over the place
            return _Parent(self._uri, self.id, getattr(self, "variation_id", None))  # pylint: disable=no-member
        return None

    def _set_resource_collection_field(self, field, value):
        query = Query(
            self._client,
            self._model_cls(field),
            parent=self._parent(),
            raw_data=value,
        )
        setattr(self, field, query)

    def _allowed_fields(self):
        first = lambda pair: pair[0]
        # Python 2 and 3
        # inefficient on Python 2 to list a map
        return (
            self._as_is_fields
            + self._date_fields
            + self._date_time_fields_utc
            + self._date_time_fields_local
            + list(map(first, self._model_fields))
            + list(map(first, self._model_collection_fields))
            + self._price_fields
            + list(map(first, self._resource_fields))
            + list(map(first, self._resource_collection_fields))
            + self._deprecated_fields
        )

    def _convert_from_resource_type(self, key, value):
        # Convert instance values into serializable objects.
        if isinstance(value, BaseModel):
            return value.to_dict()
        elif isinstance(value, Query):
            return value._to_dict()  # pylint: disable=protected-access
        elif isinstance(value, Decimal):
            return str(value)
        elif isinstance(value, (datetime.date, datetime.datetime)):
            if key in self._date_fields:
                return datetime.datetime.strftime(value, DATE_FORMAT)
            elif key in self._date_time_fields_utc:
                return datetime.datetime.strftime(value, DATE_TIME_UTC_FORMAT)
            elif key in self._date_time_fields_local:
                return datetime.datetime.strftime(value, DATE_TIME_LOCAL_FORMAT)
        else:
            return value

    def to_dict(self):
        # Python 2 and 3
        # inefficient on Python 2 to list .items
        properties = {k: v for k, v in list(self.__dict__.items()) if k in self._allowed_fields()}
        data = {}
        for key, value in list(properties.items()):
            if isinstance(value, (list, tuple)):
                data[key] = [self._convert_from_resource_type(key, a) for a in value]
            else:
                data[key] = self._convert_from_resource_type(key, value)
        return data


class RelatedResourceMixin(object):
    _related_resource_lookup = None

    def __init__(self, data):
        super(RelatedResourceMixin, self).__init__(data)

        assert self._related_resource_lookup is not None

        resource_cls = get_resource_class_from_resource_name(
            getattr(self, self._related_resource_lookup))
        resource = resource_cls({'id': self.id, 'href': self.href}, stub=True)
        setattr(self, 'resource', resource)
