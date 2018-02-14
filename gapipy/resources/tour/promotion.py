# Python 2 and 3
from __future__ import unicode_literals

from gapipy.utils import get_resource_class_from_resource_name
from gapipy.resources.base import Resource
from gapipy.resources.product import Product


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
        # Python 2 and 3
        # inefficient on Python 2 to list items()
        for k, v in list(klass.__dict__.items()):
            if 'fields' in k and isinstance(v, list):
                setattr(self, k, getattr(klass, k))

        self._resource_name = data['type']
        self._as_is_fields = self._as_is_fields + ['type', 'sub_type']

        super(PromotionProduct, self).__init__(data, **kwargs)


class Promotion(Resource):

    _resource_name = 'promotions'

    _as_is_fields = [
        'id',
        'href',
        'commission_rate',
        'currencies',
        'flags',
        'min_travellers',
        'name',
        'promotion_code',
        'room_codes',
        'terms_and_conditions',
    ]

    _date_time_fields_utc = [
        'date_created',
        'date_last_modified',
        'sale_finish_datetime',
        'sale_start_datetime',
    ]

    _date_fields = [
        'product_finish_date',
        'product_start_date',
        'sale_finish_date',
        'sale_start_date',
    ]
    _price_fields = [
        'discount_amount',
        'discount_percent',
    ]

    _model_collection_fields = [
        ('products', Product),
    ]

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
