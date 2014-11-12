import datetime
from decimal import Decimal

from gapipy import client as client_module
from gapipy.query import Query
from gapipy.utils import (
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

    def __init__(self, data, client=None):
        self._client = client or client_module.current_client
        self._raw_data = data
        self._fill_fields(data)

    def _fill_fields(self, data):
        self._raw_data = data
        first = lambda l: [pair[0] for pair in l]

        # Initially we populate base fields, as model/resource fields may rely
        # on these to be present.
        remaining_data = {}
        for field, value in data.iteritems():
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
        for field, value in remaining_data.iteritems():
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
            setattr(self, field, self._model_cls(field)(value))

    def _set_model_collection_field(self, field, value):
        model_cls = self._model_cls(field)
        items = [model_cls(m) for m in value]
        setattr(self, field, items)

    def _set_resource_field(self, field, value):
        stub = None

        if isinstance(value, list):
            stub = []
            for v in value:
                stub.append(self._model_cls(field)(v, stub=True))
        elif value:
            stub = self._model_cls(field)(value, stub=True)
        setattr(self, field, stub)

    def _set_resource_collection_field(self, field, value):
        is_parent_resource = getattr(self, '_is_parent_resource', None)
        if is_parent_resource:
            parent = (self._resource_name, self.id)
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
        properties = {k: v for k, v in self.__dict__.iteritems() if k in self._allowed_fields()}
        data = {}
        for key, value in properties.iteritems():
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
