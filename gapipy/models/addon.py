from .base import BaseModel, RelatedResourceMixin
from ..utils import enforce_string_type


class AddOn(BaseModel, RelatedResourceMixin):
    _as_is_fields = ['max_days', 'min_days', 'product']
    _date_fields = ['start_date', 'finish_date', 'halt_booking_date', 'request_space_date']
    _resource_fields = []

    @enforce_string_type
    def __repr__(self):
        return '<{0} ({1})>'.format(self.__class__.__name__, self.product.name)

    # product is marked as as-is, so we can turn it into a dynamically-typed resource, based on product['type']
    # Is there a better way?
    def _fill_fields(self, data):
        super(AddOn, self)._fill_fields(data)
        r = {
            'activities': 'Activity',
            'accommodations': 'Accommodation',
            'transports': 'Transport',
            'single_supplements': 'SingleSupplement',
        }.get(self.product['type'])
        if r:
            self._resource_fields += [('product', r)]
            self._set_resource_field('product', self.product)
