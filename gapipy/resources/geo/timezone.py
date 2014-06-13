from __future__ import unicode_literals

from ..base import Resource


class Timezone(Resource):

    _resource_name = 'timezones'

    _as_is_fields = [
        'id', 'href', 'code', 'gmt_offset', 'dst_offset',
    ]
    _date_time_fields_utc = ['date_created', 'date_last_modified']
