from ..base import Resource


class AgencyChain(Resource):

    _resource_name = 'agency_chains'
    _as_is_fields = ['id', 'href', 'name', 'flags', 'communication_preferences', 'payment_options', 'agencies']
    _date_time_fields_local = ['date_created']
