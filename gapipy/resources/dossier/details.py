from __future__ import unicode_literals

from ...models.base import BaseModel
from ...utils import enforce_string_type


class DossierDetailType(BaseModel):
    _as_is_fields = ['code', 'label', 'description']

    @enforce_string_type
    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.label)


class DossierDetail(BaseModel):
    _as_is_fields = ['body']

    _model_fields = [
        ('detail_type', DossierDetailType),
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.detail_type)


class DossierDetailsMixin(object):
    """
    Helpers for accessing specific details by type (`code`)
    """
    def _get_detail(self, code, default=None):
        """
        Returns the first detail object with for the given detail_type `code`
        """
        details = [d for d in self.details if d.detail_type.code == code]
        return details[0] if details else default

    def _get_detail_body(self, code):
        """
        Returns the body of a given detail_type's `code`
        """
        detail = self._get_detail(code, None)
        if detail:
            return detail.body

    @property
    def summary(self):
        return self._get_detail_body('COMMON__SUMMARY')

    @property
    def description(self):
        return self._get_detail_body('COMMON__DESCRIPTION')
