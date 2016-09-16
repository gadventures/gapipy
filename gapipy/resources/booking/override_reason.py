#!/usr/bin/env python
from __future__ import unicode_literals

from ..base import Resource
from ...utils import enforce_string_type


class OverrideReason(Resource):

    _resource_name = 'override_reasons'

    _as_is_fields = ['id', 'href', 'label', 'code']

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.label)
