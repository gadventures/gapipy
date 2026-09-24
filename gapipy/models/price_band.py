from .base import BaseModel


class DateRange(BaseModel):
    _date_fields = ['start_date', 'finish_date']

    def _fill_date_fields(self, data):
        for field in self._date_fields:
            if field not in data:
                data[field] = None
        return super(DateRange, self)._fill_date_fields(data)


class Price(BaseModel):
    _as_is_fields = ['currency']
    _price_fields = ['amount', 'deposit']

    @property
    def _model_collection_fields(self):
        from .price_promotion import PricePromotion
        return [('promotions', PricePromotion)]


class DeparturePrice(Price):
    @property
    def _price_fields(self):
        return super(DeparturePrice, self)._price_fields + [
            'approximate_amount_with_local_payments',
        ]

    @property
    def _model_collection_fields(self):
        from .price_promotion import DeparturePricePromotion
        return [('promotions', DeparturePricePromotion)]


class PriceBand(BaseModel):
    _as_is_fields = [
        'code', 'max_age', 'max_travellers', 'min_age',
        'min_travellers', 'name',
    ]

    @property
    def _model_collection_fields(self):
        return [('prices', Price)]

    def available_currencies(self):
        # Python 2 and 3
        # inefficient on Python 2 to list keys()
        return list(self.prices.keys())


class DeparturePriceBand(PriceBand):

    @property
    def _model_collection_fields(self):
        return [('prices', DeparturePrice)]


class SeasonalPriceBand(PriceBand):

    @property
    def _model_collection_fields(self):
        return super(SeasonalPriceBand, self)._model_collection_fields + [
            ('season_dates', DateRange),
            ('blackout_dates', DateRange),
        ]


class PP2aPrice(BaseModel):
    _as_is_fields = ['currency']
    _price_fields = ['amount', 'approximate_amount_with_local_payments']
