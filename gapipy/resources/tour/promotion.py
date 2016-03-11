from __future__ import unicode_literals

from ...utils import get_resource_class_from_resource_name
from ..base import Resource, Product


class PromotionProduct(Resource):
    """
    The `products` referenced in a Promotion object are not valid resources (due
    to the existence of `type`) so they must be wrapped in this model.

    When the resource is fixed, the hacks here can simply be replaced with
    `gapipy.models.base.RelatedResourceMixin`
    """
    def __init__(self, data, **kwargs):
        # Fetch the resource class using the `type`, and then derive field
        # attributes from that class.
        klass = get_resource_class_from_resource_name(data['type'])
        for k, v in klass.__dict__.items():
            if 'fields' in k and isinstance(v, list):
                setattr(self, k, getattr(klass, k))

        self._resource_name = data['type']
        self._as_is_fields = self._as_is_fields + ['type', 'sub_type']

        super(PromotionProduct, self).__init__(data, **kwargs)


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
            stub = PromotionProduct(product, client=self._client, stub=True)
            product_stubs.append(stub)
        setattr(self, field, product_stubs)
