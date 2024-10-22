from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


class CoinResponse(BaseModel):
    coin_name: str
    symbol: str
    coin_price: float
    coin_price_dolar: float
    date_consult: datetime = Field(examples=["2022-12-01 01:01:01"])

    @field_serializer("date_consult")
    def date_consult_format(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")
