from __future__ import unicode_literals

from gapipy.resources.base import Resource


class CancellationTerm(Resource):
    _resource_name = "cancellation_terms"

    _as_is_fields = [
        "id",
        "href",
        "name",
        "terms_url",
        "terms",
    ]

    _resource_fields = [
        ("departure", "Departure"),
        ("booking_company", "BookingCompany"),
    ]
