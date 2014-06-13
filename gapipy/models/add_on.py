from .base import BaseModel, RelatedResourceMixin


class AddOn(BaseModel, RelatedResourceMixin):
    _as_is_fields = [
        'id', 'href', 'max_days', 'min_days', 'name', 'type', 'sub_type'
    ]
    _date_fields = ['start_date', 'finish_date']
    _related_resource_lookup = 'type'

    def __repr__(self):
        return '<{0} ({1})>'.format(self.__class__.__name__, self.name)
