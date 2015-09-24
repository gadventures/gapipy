from __future__ import unicode_literals


from ..base import Product
from ..dossier import ActivityDossier


class Activity(Product):

    _resource_name = 'activities'
    _is_listable = False

    _as_is_fields = [
        'id', 'href', 'availability', 'name', 'description', 'product_line',
        'sku', 'type', 'sub_type', 'requirements',
    ]
    _date_fields = ['start_date', 'finish_date']
    _date_time_fields_utc = ['date_created', 'date_last_modified']

    @property
    def _model_collection_fields(self):
        from ...models import PriceBand
        return [
            ('price_bands', PriceBand),
        ]

    _resource_fields = [('activity_dossier', ActivityDossier)]
