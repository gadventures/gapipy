from __future__ import unicode_literals

from ..base import Resource


class Document(Resource):
    _resource_name = 'documents'
    _is_listable = False

    _as_is_fields = ['id', 'href', 'mime_type', 'content', 'type', 'audience']
    _date_time_fields_utc = ['date_created']
    _resource_fields = [
        ('booking', 'Booking'),
    ]


class Invoice(Resource):
    _resource_name = 'invoices'
    _is_listable = False

    _as_is_fields = ['id', 'href', 'audience']
    _date_time_fields_utc = ['date_created']
    _resource_fields = [
        ('document', Document),
        ('booking', 'Booking'),
    ]
