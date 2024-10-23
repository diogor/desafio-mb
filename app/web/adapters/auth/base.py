from abc import ABCMeta, abstractmethod
from datetime import timedelta


class Oauth2Base(metaclass=ABCMeta):
    @abstractmethod
    def verify_password(
        self, plain_password: str | bytes, hashed_password: str | bytes
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_password_hash(self, password: str | bytes) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, str]:
        raise NotImplementedError
