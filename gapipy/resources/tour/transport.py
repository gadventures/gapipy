from __future__ import unicode_literals

from ...models import Address, SeasonalPriceBand

from ..base import Product


class Transport(Product):

    _resource_name = 'transports'
    _is_listable = False

    _as_is_fields = [
        'id', 'href', 'availability', 'name', 'product_line', 'sku', 'type', 'sub_type'
    ]
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _model_fields = [('start_address', Address), ('finish_address', Address)]
    _model_collection_fields = [('price_bands', SeasonalPriceBand)]
