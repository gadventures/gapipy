from __future__ import unicode_literals

from gapipy.resources.base import Resource

from .flex_tier import FlexTier


class FlexPlan(Resource):
    _resource_name = "flex_plans"

    _as_is_fields = [
        "id",
        "href",
        "name",
        "product_line",
        "sku",
        "type",
        "sub_type",
        "availability",
        "rooms",
        "percent",
    ]

    _date_fields = [
        "start_date",
        "finish_date",
    ]

    _date_time_fields_utc = [
        "date_created",
    ]

    _resource_fields = [
        ("booking_company", "BookingCompany"),
        ("departure", "Departure"),
        ("flex_tier", FlexTier),
        ("flex_cancellation_terms", "FlexCancellationTerm"),
    ]
