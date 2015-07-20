from gapipy.resources.base import Resource


class DeclinedReason(Resource):
    _resource_name = 'declined_reasons'

    _as_is_fields = ['id', 'href', 'service', 'channels', 'name']
