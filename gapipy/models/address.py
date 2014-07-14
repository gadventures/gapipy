from .base import BaseModel


class Address(BaseModel):
    _as_is_fields = ['city', 'latitude', 'longitude', 'postal_zip', 'street']
    _resource_fields = [
        ('state', 'State'),
        ('country', 'Country')
    ]

    def __repr__(self):
        return '<{0}: {1}, {2}>'.format(
            self.__class__.__name__, self.city, self.country.name)
