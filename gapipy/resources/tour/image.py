# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..base import Resource
from ...models.base import BaseModel


MAP_TYPE = 'MAP'
OTHER_TYPE = 'OTHER'

IMAGE_TYPES = (
    MAP_TYPE,
    OTHER_TYPE,
)

class ImageFile(BaseModel):
    _as_is_fields = [
        'url', 'data', 'mime_type', 'exif',
    ]


class Image(Resource):

    _resource_name = 'images'

    _as_is_fields = [
        'id', 'href', 'modification', 'description', 'keywords',
        'attribution', 'channels', 'variations', 'type',
    ]
    _date_time_fields_local = ['date_created', 'date_last_modified']
    _resource_fields = [('original', 'Image')]
    _model_fields = [('file', ImageFile)]
