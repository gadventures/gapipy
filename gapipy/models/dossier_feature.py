from .base import BaseModel

class DossierFeatureParent(BaseModel):
    _as_is_fields = ['id', 'label', 'code', 'description']

class DossierFeatureChild(BaseModel):
    _as_is_fields = ['id', 'label', 'code', 'description']
