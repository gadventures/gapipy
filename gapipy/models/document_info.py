from .base import BaseModel


class DocumentInfo(BaseModel):
    """Represents a document, without its content"""
    _as_is_fields = ['id', 'href', 'mime_type', 'type']
    _date_time_fields_utc = ['date_created']
    _resource_fields = [
        ('booking', 'Booking'),
    ]
