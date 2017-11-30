from ..resources.base import Resource
from ..utils import get_resource_class_from_resource_name


class PricePromotion(Resource):
    """
    The `promotions` referenced in a `Price` are not valid, as they include an
    `amount` field that is not part of the Promotion object.

    Thus, this intermediatary model must be used to represent a pseudo-Resource.
    """
    def __init__(self, data, **kwargs):
        self._resource_name = 'promotions'

        klass = get_resource_class_from_resource_name('promotions')

        promotion_field_types = [
            '_as_is_fields',
            '_date_time_fields_utc',
            '_date_fields',
            '_price_fields',
            '_model_collection_fields',
            '_resource_collection_fields',
        ]

        # Python 2 and 3
        # inefficient on Python 2 to list items()
        for field_type in promotion_field_types:
            value = getattr(klass, field_type, None)
            if value:
                setattr(self, field_type, value)

        if getattr(klass, '_is_parent_resource', None):
            setattr(self, '_is_parent_resource', klass._is_parent_resource)

        super(PricePromotion, self).__init__(data, **kwargs)

        # Add the "fake" amount field.
        if 'amount' not in self._price_fields:
            self._price_fields.append('amount')
            setattr(self, 'amount', data['amount'])
