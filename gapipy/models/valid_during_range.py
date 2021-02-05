# pylint: disable=no-member
import datetime

from gapipy.utils import enforce_string_type

from .base import BaseModel


class ValidDuringRange(BaseModel):
    _date_fields = [
        'end_date',
        'start_date',
    ]

    def is_expired(self):
        return not self.is_valid_during_range(datetime.date.today(), None)

    def is_valid_today(self):
        return self.is_valid_on_date(datetime.date.today())

    def is_valid_during_range(self, start_date, end_date):
        if start_date and not end_date:
            return self.is_valid_on_or_after_date(start_date)

        if not start_date and end_date:
            return self.is_valid_on_or_before_date(end_date)

        if not start_date and not end_date:
            return self.is_valid_sometime()

        if start_date == end_date:
            return self.is_valid_on_date(start_date)

        # start_date and end_date are both not None and not equal
        return (
            start_date <= end_date
        ) and (
            self.is_valid_sometime()
        ) and all([
            self.start_date is None or self.start_date <= end_date,
            self.end_date is None or self.end_date >= start_date,
        ])

    def is_valid_on_or_after_date(self, date):
        return (
            self.end_date is None
        ) or (
            self.start_date is None and
            self.end_date >= date
        ) or (
            self.start_date is not None and
            self.start_date <= self.end_date and
            self.end_date >= date
        )

    def is_valid_on_or_before_date(self, date):
        return (
            self.start_date is None
        ) or (
            self.end_date is None and
            self.start_date <= date
        ) or (
            self.end_date is not None and
            self.start_date <= self.end_date and
            self.start_date <= date
        )

    def is_valid_on_date(self, date):
        return all([
            self.start_date is None or self.start_date <= date,
            self.end_date is None or self.end_date >= date,
        ])

    def is_valid_sometime(self):
        return (
            self.start_date is None or
            self.end_date is None or
            self.start_date <= self.end_date
        )

    @enforce_string_type
    def __repr__(self):
        return '<{} ({} - {})>'.format(self.__class__.__name__, self.start_date, self.end_date)
