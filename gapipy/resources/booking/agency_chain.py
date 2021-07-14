# Python 2 and 3
from __future__ import unicode_literals

from gapipy.resources.base import Resource
from gapipy.resources.booking_company import BookingCompany


class AgencyChain(Resource):
    _resource_name = "agency_chains"
    _is_parent_resource = True

    _as_is_fields = [
        "agent_notifications",
        "communication_preferences",
        "flags",
        "href",
        "id",
        "name",
        "online_preferences",
        "passenger_notifications",
        "payment_options",
    ]

    _date_time_fields_local = [
        "date_created",
        "date_last_modified",
    ]

    _resource_fields = [
        ("booking_company", BookingCompany),
    ]

    _resource_collection_fields = [
        ("agencies", "Agency"),
    ]
