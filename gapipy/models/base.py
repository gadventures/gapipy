from decimal import Decimal
from itertools import ifilterfalse
import datetime

from gapipy.query import Query
from gapipy.utils import (
    enforce_string_type,
    get_resource_class_from_class_name,
    get_resource_class_from_resource_name,
)

DATE_FORMAT = '%Y-%m-%d'
DATE_TIME_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATE_TIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M:%S"


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
        self._raw_data = data
        self._fill_fields(data)

    def _fill_fields(self, data):
        self._raw_data = data
        first = lambda l: [pair[0] for pair in l]

        # Initially we populate base fields, as model/resource fields may rely
        # on these to be present.
        remaining_data = {}
        for field, value in data.items():
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
        for field, value in remaining_data.items():
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
        if isinstance(model_cls, basestring):
            model_cls = get_resource_class_from_class_name(model_cls)
        return model_cls

    def _set_model_field(self, field, value):
        if value is None:
            setattr(self, field, None)
        else:
            setattr(self, field, self._model_cls(field)(value, client=self._client))

    def _set_model_collection_field(self, field, value):
        from functools import partial
        from gapipy.resources.base import Resource

        model_cls = self._model_cls(field)

        # If `model_cls` can be of three type: a Resource, a BaseModel that
        # isn't a Resource, or a wrapped DictToModel instance. If it is a
        # Resource, then we pass in the `stub` kwarg.
        #
        # We first check whether `model_cls` is a DictToModel or not (as
        # opposed to the simpler, two branch "if Resource do this else do
        # that"), since `issubclass` only accepts classes as argument.
        if isinstance(model_cls, partial):
            # dict-to-model instance
            items = [model_cls(m) for m in value]
        elif issubclass(model_cls, Resource):
            items = [model_cls(m, client=self._client, stub=True) for m in value]
        else:
            items = [model_cls(m, client=self._client) for m in value]

        setattr(self, field, items)

    def _set_resource_field(self, field, value):
        if value is None:
            setattr(self, field, None)
        else:
            setattr(self, field, self._model_cls(field)(value, client=self._client, stub=True))

    def _set_resource_collection_field(self, field, value):
        is_parent_resource = getattr(self, '_is_parent_resource', None)
        if is_parent_resource:
            # FIXME: variation_id is hardcoded all over the client. This should
            # not be the case, but is a neccessity for now.
            parent = (
                self._resource_name,
                self.id,
                getattr(self, 'variation_id', None),
            )

        else:
            parent = None

        raw_data = value
        query = Query(self._client, self._model_cls(field), parent=parent, raw_data=raw_data)
        setattr(self, field, query)

    def _allowed_fields(self):
        first = lambda pair: pair[0]
        return (
            self._as_is_fields
            + self._date_fields
            + self._date_time_fields_utc
            + self._date_time_fields_local
            + map(first, self._model_fields)
            + map(first, self._model_collection_fields)
            + self._price_fields
            + map(first, self._resource_fields)
            + map(first, self._resource_collection_fields)
            + self._deprecated_fields
        )

    def _convert_from_resource_type(self, key, value):
        # Convert instance values into serializable objects.
        if isinstance(value, BaseModel):
            return value.to_dict()
        elif isinstance(value, Query):
            return value._to_dict()
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
        properties = {k: v for k, v in self.__dict__.items() if k in self._allowed_fields()}
        data = {}
        for key, value in properties.items():
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


class DictToModel(object):
    """
    A simple container that is used by `utils.dict_to_model` to help create
    dot-accessible models without being explicit about field definitions.

    This class simply iterates over any complex values and recursively creates
    new objects for those their respective keys, allowing the entire path to be
    dot-accessible.
    """
    def __init__(self, data, class_name=None):
        self._class_name = self._humanize(class_name) if class_name else ''

        # Add any shallow data to this object as primitive types.
        shallow = self._shallow(data)
        self.__dict__.update(shallow)

        # Anything that will contain nested values that need to be dot
        # accessible receive treatment of having its own class representation.
        for k, v in self._deep(data).items():
            if isinstance(v, (list, tuple)):
                value = [DictToModel(i, class_name=k) for i in v]
            else:
                value = DictToModel(v, class_name=k)
            setattr(self, k, value)

    def __str__(self):
        return self._class_name

    @enforce_string_type
    def __repr__(self):
        return '<{}>'.format(self.__str__())

    def _humanize(self, class_name):
        return class_name.replace("_", " ").title()

    def _get_data(self, data):
        """ Use as predicate for _shallow, _deep """
        return isinstance(data[1], (dict, list))

    def _shallow(self, data):
        return {k: v for k, v in ifilterfalse(self._get_data, data.items())}

    def _deep(self, data):
        return {k: v for k, v in filter(self._get_data, data.items())}
