from __future__ import unicode_literals

from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource


class LocalPaymentSellCurrency(BaseModel):
    _as_is_fields = [
        "currency",
    ]
    _price_fields = [
        "amount",
        "maximum_amount",
        "minimum_amount",
    ]


class LocalPayment(Resource):
    _resource_name = "local_payments"

    _is_listable = False

    _as_is_fields = [
        "id",
        "href",
        "currency",
        "description",
        "included_in_total",
        "label",
        "price_type",
    ]
    _date_fields = [
        "rate_as_of",
    ]
    _price_fields = [
        "amount",
        "maximum_amount",
        "minimum_amount",
    ]
    _model_collection_fields = [
        ("sell_currencies", LocalPaymentSellCurrency),
    ]
