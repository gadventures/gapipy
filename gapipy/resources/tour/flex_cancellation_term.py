from __future__ import unicode_literals

from gapipy.resources.base import Resource

from .flex_plan import FlexPlan


class FlexCancellationTerm(Resource):
    _resource_name = "flex_cancellation_terms"

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
        ("flex_plan", FlexPlan),
    ]
