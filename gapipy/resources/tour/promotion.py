from __future__ import unicode_literals

from ...utils import get_resource_class_from_resource_name
from ..base import Resource, Product


class Promotion(Resource):

    _resource_name = 'promotions'

    _as_is_fields = [
        'id', 'href', 'commission_rate', 'currencies', 'flags',
        'min_travellers', 'name', 'promotion_code', 'room_codes',
        'terms_and_conditions',
    ]

    _date_fields = [
        'product_start_date', 'product_finish_date',
        'sale_start_date', 'sale_finish_date'
    ]
    _price_fields = ['discount_amount', 'discount_percent']
    _model_collection_fields = [('products', Product)]

    def _set_model_collection_field(self, field, data):
        # Only products needs special treatment.
        if field != 'products':
            return super(Promotion, self)._set_model_collection_field(field, data)

        product_stubs = []
        # Each product can be a different resource, so derive the resource from
        # the "type" within the stubbed object.
        for product in data:
            product_type = product['type']
            resource_cls = get_resource_class_from_resource_name(product_type)
            stub = resource_cls(product, stub=True)
            product_stubs.append(stub)
        setattr(self, field, product_stubs)
