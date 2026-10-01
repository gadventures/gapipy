from __future__ import unicode_literals

from gapipy.resources.base import Resource


class ServiceCancellationTerm(Resource):
    _resource_name = "service_cancellation_terms"

    _as_is_fields = [
        "id",
        "href",
        "terms",
        "total_gross_amount",
        "lifetime_deposit_amount",
        "refundable_amount",
        "windows",
    ]

    _date_time_fields_utc = [
        "date_created",
    ]

    _resource_fields = [
        ("departure_service", "DepartureService"),
    ]
