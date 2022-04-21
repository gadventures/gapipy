# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from gapipy.exceptions import EmptyPartialUpdateError
from gapipy.models.base import BaseModel
from gapipy.request import APIRequestor
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

    def fetch(self, httperrors_mapped_to_none=None):
        """
        httperrors_mapped_to_none is a list of HTTP errors we will silently absorb (i.e.
        not float up). This brings back behavior prior to 2.25.0.
        ref: https://github.com/gadventures/gapipy/pull/119
        """
        logger.info('Fetching %s/%s', self._resource_name, self.id)

        # Fetch the resource using the client bound on it, which handles cache get/set.
        resource_obj = getattr(self._client, self._resource_name).get(
            self.id,
            variation_id=getattr(self, 'variation_id', None),
            httperrors_mapped_to_none=httperrors_mapped_to_none)
        if resource_obj:
            self._fill_fields(resource_obj._raw_data)
            self.is_stub = False

        return self

    @classmethod
    def create(cls, client, data_dict, headers=None):
        request = APIRequestor(client, cls)
        response = request.create(json.dumps(data_dict), headers=headers)
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

        # payload to send
        data = self.to_dict()

        # when making a partial (PATCH) request, ensure we only include values
        # changed on self compared to the initial raw response received from
        # the G API.
        #
        # Added (2.35.0): If the change computed results in an empty data
        #                 dictionary we'll raise a EmptyPartialUpdateError
        if partial:
            data = {k: v for k, v in data.items() if self._raw_data.get(k) != v}
            if not data:
                raise EmptyPartialUpdateError

        return request.update(self.id, json.dumps(data), partial=partial)

    def _create(self):
        request = APIRequestor(self._client, self)
        return request.create(self.to_json())

    def save(self, partial=False):
        """
        Save the current state of the resource to GAPI. If a new instance, it
        will result in a POST request to the G API, otherwise depending on the
        value of partial, will result in a PUT request if partial is `False`
        otherwise a PATCH request.

        Added (2.35.0): we check if a partial update threw an exception and
                        re-raise it if the client has been configured to do so
                        via raise_on_empty_update config option.
        """

        # update if we have an `id` value
        #
        # due to the explicit check for `id` in __getattr__, we need to check
        # the __dict__ directly for the `id` attribute... 🐔 & 🥚 situation
        is_update = 'id' in self.__dict__ and self.__dict__['id']
        if is_update:
            try:
                result = self._update(partial=partial)
            except EmptyPartialUpdateError:
                if self._client.raise_on_empty_update:
                    raise
                # return early to avoid calling _fill_fields unnecessarily
                return self
        else:
            result = self._create()

        # set result fields as attributes
        self._fill_fields(result)
        return self
