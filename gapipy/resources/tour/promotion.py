from __future__ import unicode_literals

from ...utils import (
    get_resource_class_from_class_name, get_resource_class_from_resource_name
)
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
    _resource_collection_fields = [('products', Product)]

    def _fill_resource_collection_fields(self, data):
        for field, resource_cls in self._resource_collection_fields:
            if isinstance(resource_cls, basestring):
                resource_cls = get_resource_class_from_class_name(resource_cls)

            products = data[field]
            if products:
                product_type = products[0]['type']
                resource_cls = get_resource_class_from_resource_name(product_type)
                product_stubs = [resource_cls(p, stub=True) for p in products]
                setattr(self, field, product_stubs)
            else:
                setattr(self, field, [])
