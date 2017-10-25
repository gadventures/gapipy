from ..base import Resource


class AgencyChain(Resource):

    _resource_name = 'agency_chains'
    _as_is_fields = [
        'id',
        'href',
        'name',
        'flags',
        'communication_preferences',
        'payment_options',
        'agencies',
        'passenger_notifications',
        'agent_notifications',
    ]
    _date_time_fields_local = ['date_created']
