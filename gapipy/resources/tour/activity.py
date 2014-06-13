from __future__ import unicode_literals

from ...models import PriceBand

from ..base import Product


class Activity(Product):

    _resource_name = 'activities'
    _is_listable = False

    # TODO: Move `activity_dossier` to `_resource_fields` once the
    # ActivityDossier resource is implemented.
    _as_is_fields = [
        'id', 'href', 'availability', 'name', 'description', 'product_line',
        'sku', 'type', 'sub_type', 'requirements', 'activity_dossier',
    ]
    _date_fields = ['start_date', 'finish_date']
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _model_collection_fields = [('price_bands', PriceBand)]
