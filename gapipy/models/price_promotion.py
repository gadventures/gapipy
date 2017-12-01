from gapipy.utils import get_resource_class_from_class_name

# get the Promotion class
#
# NOTE: this is intentional, and needed to ensure we
#       are loading the `correct` Promotion class
Promotion  = get_resource_class_from_class_name('Promotion')


class PricePromotion(Promotion):
    """
    This extends the definition of the Promotion class
    adding the ``amount`` price field, for use in the
    `Prices` model
    """
    @property
    def _price_fields(self):
        return super(PricePromotion, self)._price_fields + ['amount']
