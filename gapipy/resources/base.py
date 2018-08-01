# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from gapipy.request import APIRequestor
from gapipy.models.base import BaseModel
from gapipy.utils import enforce_string_type


logger = logging.getLogger(__name__)


class Resource(BaseModel):

    _resource_name = None
    _is_parent_resource = False
    _is_listable = True  # True if resource can be listed/queried (i.e /{resource_name} is an endpoint)
    _uri = None

    def __init__(self, data, stub=False, client=None):
        self.is_stub = stub
        if not self._uri:
            self._uri = self._resource_name
        super(Resource, self).__init__(data, client)

    @classmethod
    def options(cls, client):
        return APIRequestor(client, cls).options()

    def fetch(self):
        logger.info('Fetching %s/%s', self._resource_name, self.id)
        self.is_stub = False

        # Fetch the resource using the client bound on it, which handles cache get/set.
        resource_obj = getattr(self._client, self._resource_name).get(
            self.id,
            variation_id=getattr(self, 'variation_id', None))
        if resource_obj:
            self._fill_fields(resource_obj._raw_data)
        return self

    @classmethod
    def create(cls, client, data_dict):
        request = APIRequestor(client, cls)
        response = request.create(json.dumps(data_dict))
        return cls(response, client=client)

    def __getattr__(self, name):
        # If we try to access a field that's allowed, and this resource is a
        # stub, we need to fetch it.
        if name == 'id':
            raise AttributeError(
                'No id found for Resource %s. Possibly caused due to bad or stale data.' % self._resource_name
            )

        if name in self._allowed_fields() and self.is_stub:
            self.fetch()
            return self.__getattribute__(name)

        raise AttributeError("%r has no field %r available" % (type(self).__name__, name))

    @enforce_string_type
    def __repr__(self):
        if self.is_stub:
            return '<{}: {} (stub)>'.format(self.__class__.__name__, self.id)
        else:
            return '<{}: {}>'.format(self.__class__.__name__, self.id)

    def __hash__(self):
        return hash('{}{}'.format(self.__class__.__name__, self.id))

    def __eq__(self, other):
        # Same resource name and ID determine equality
        return (
            self._resource_name == getattr(other, '_resource_name', None)
            and self.id == other.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_json(self):
        return json.dumps(self.to_dict())

    def _update(self, partial=False):
        request = APIRequestor(self._client, self)

        data = self.to_dict()
        if partial:
            # .items isn't effecient in Python 2
            data = {k: v for k, v in data.items() if self._raw_data.get(k) != v}

        return request.update(self.id, json.dumps(data), partial=partial)

    def _create(self):
        request = APIRequestor(self._client, self)
        return request.create(self.to_json())

    def save(self, partial=False):
        # due to the explicit check for `id` in __getattr__, we
        # need to check the __dict__ directly for the `id`
        # attribute... 🐔 & 🥚 situation
        if 'id' in self.__dict__ and self.__dict__['id']:
            result = self._update(partial=partial)
        else:
            result = self._create()
        # set reslt fields as attributes
        self._fill_fields(result)
        return self
