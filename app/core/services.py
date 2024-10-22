import requests
from requests.exceptions import RequestException
from datetime import datetime
from functools import reduce
from app.core.models import APIInfo
from app.settings import get_apis
from app.web.response import CoinResponse


def _resolve_key(data: dict | list, key_path: str):
    keys = key_path.split(".")

    def _reduce_func(acc, key):
        if isinstance(key, int):
            return acc[key]
        return acc.get(key, {})

    value = reduce(_reduce_func, keys, data)

    return value


def _get_data(api_defs: APIInfo, data: dict | list) -> dict:
    response = {}

    response["coin_name"] = (
        _resolve_key(data, api_defs.coin_name) if api_defs.coin_name else None
    )
    response["symbol"] = (
        _resolve_key(data, api_defs.symbol) if api_defs.symbol else None
    )
    response["coin_price"] = _resolve_key(data, api_defs.coin_price)
    response["coin_price_dolar"] = _resolve_key(data, api_defs.coin_price)
    response["date_consult"] = datetime.now()

    return response


def get_symbol_price(symbol: str) -> CoinResponse | None:
    apis = get_apis()
    resp = None
    req = requests.Response()
    for api in apis:
        try:
            req = requests.get(api["uri"].format(api.get("symbols", {})[symbol]))
            if req.status_code != 200:
                print(
                    f"API {api['name']} returned status code {req.status_code}: {req.reason}"
                )
                continue
        except KeyError:
            print(f"Coin {symbol} not found on API {api['name']}")
            continue
        except RequestException as e:
            print(e)
            continue

        api_info = APIInfo(
            id=api["id"],
            name=api["name"],
            uri=api["uri"],
            coin_name=api["coin_name"],
            symbol=api["symbol"],
            coin_price=api["coin_price"],
        )

        data = _get_data(api_info, req.json())

        resp = CoinResponse(
            coin_name=data["coin_name"] or symbol,
            symbol=data["symbol"] or symbol,
            coin_price=data["coin_price"],
            coin_price_dolar=data["coin_price_dolar"],
            date_consult=data["date_consult"],
        )
        break

    return resp
