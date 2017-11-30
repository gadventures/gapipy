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

        # Python 2 and 3
        # inefficient on Python 2 to list items()
        for k, v in list(klass.__dict__.items()):
            if 'fields' in k and isinstance(v, list):
                setattr(self, k, getattr(klass, k))
            if '_is_parent_resource' in k:
                setattr(self, k, v)

        super(PricePromotion, self).__init__(data, **kwargs)

        # Add the "fake" amount field.
        self._price_fields.append('amount')
        setattr(self, 'amount', data['amount'])
