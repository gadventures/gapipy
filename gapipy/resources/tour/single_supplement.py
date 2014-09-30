from __future__ import unicode_literals

from ...models import PriceBand

from ..base import Product


class SingleSupplement(Product):

    _resource_name = 'single_supplements'
    _is_listable = False

    _as_is_fields = ['id', 'href', 'availability', 'name', 'product_line', 'sku', 'type', 'sub_type']
    _date_fields = ['start_date', 'finish_date']
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _model_collection_fields = [('price_bands', PriceBand)]
    _resource_fields = [('departure', 'Departure')]
