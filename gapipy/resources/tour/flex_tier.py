from __future__ import unicode_literals

from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource


class WindowEffectiveDays(BaseModel):
    _as_is_fields = [
        "from_start_date",
        "to_start_date",
    ]


class FlexTierTermWindow(BaseModel):
    _model_fields = [
        ("effective_days", WindowEffectiveDays)
    ]
    # this converts these values to decimal.Decimal objects
    _price_fields = [
        "refund_percent",  
        "travel_credit_percent",
    ]


class FlexTierTerm(BaseModel):
    _as_is_fields = [
        "lifetime_deposit_retention",
    ]
    _model_collection_fields = [
        ("windows", FlexTierTermWindow),
    ]


class FlexTier(Resource):
    _resource_name = "flex_tiers"

    _as_is_fields = [
        "id",
        "href",
        "name",
        "product_line",
    ]

    _date_time_fields_utc = [
        "date_created",
    ]

    _model_fields = [
        ("terms", FlexTierTerm),
    ]

    _resource_fields = [
        ("booking_company", "BookingCompany"),
    ]
