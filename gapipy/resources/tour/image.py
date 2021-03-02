# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource


class ImageFile(BaseModel):
    _as_is_fields = [
        'url',
        'data',
        'mime_type',
        'exif',
    ]


class Image(Resource):

    _resource_name = 'images'

    _as_is_fields = [
        'id',
        'href',
        'variation_id',
        'attribution',
        'channels',
        'description',
        'keywords',
        'modification',
        'type',
        'variations',
    ]
    _date_time_fields_local = [
        'date_created',
        'date_last_modified',
    ]
    _resource_fields = [
        ('original', 'Image'),
    ]
    _model_fields = [
        ('file', ImageFile),
    ]
