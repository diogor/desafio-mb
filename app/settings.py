import logging
import configparser
from environs import Env

env = Env()
env.read_env()

APIS_CONFIG = configparser.ConfigParser()
SYMBOLS_CONFIG = configparser.ConfigParser()

CACHE_SECONDS = env.int("CACHE_SECONDS", 10)
DATABASE_URL = env("DATABASE_URL", "sqlite:///app.db")
SECRET_KEY = env("SECRET_KEY", "secret")
JWT_ALGORITHM = env("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", 15)


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    filename="application.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_apis():
    APIS_CONFIG.read("config/apis.ini")
    SYMBOLS_CONFIG.read("config/symbols.ini")

    return [
        {
            "id": s,
            "name": APIS_CONFIG[s]["name"],
            "uri": APIS_CONFIG[s]["uri"],
            "coin_name": APIS_CONFIG[s].get("coin_name"),
            "symbol": APIS_CONFIG[s].get("symbol"),
            "coin_price": APIS_CONFIG[s]["coin_price"],
            "symbols": SYMBOLS_CONFIG[s],
        }
        for s in APIS_CONFIG.sections()
    ]
