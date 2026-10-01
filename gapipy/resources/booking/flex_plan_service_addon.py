from __future__ import unicode_literals

from gapipy.resources.base import Resource


class FlexPlanServiceAddon(Resource):
    _resource_name = "flex_plan_service_addons"

    _as_is_fields = [
        "id",
        "href",
        "type",
        "order_url",
        "products",
        "support_url",
        "terms_url",
    ]

    _resource_fields = [
        ("booking", "Booking"),
        ("customer", "Customer"),
        ("flex_plan_service", "FlexPlanService"),
    ]
