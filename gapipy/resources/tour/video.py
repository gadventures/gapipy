# -*- coding: utf-8 -*-
# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource



class Video(Resource):

    _resource_name = 'videos'

    _as_is_fields = [
        'id',
        'href',
        'url',
        'code',
        'source',
        'title',
        'description',
        'image',
    ]
