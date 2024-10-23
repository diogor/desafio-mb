from typing import Optional
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select
from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.models import commit, engine, Session
from app.models.auth import User
from app.web.adapters.auth.base import Oauth2Base
from app.web.adapters.auth.token_auth import Oauth2TokenAuth


class UserRepository:
    auth_adapter: Oauth2Base

    def __init__(self, auth_adapter: Oauth2Base = Oauth2TokenAuth()):
        self.auth_adapter = auth_adapter

    def get_user_by_username(self, username: str) -> User:
        with Session(engine) as session:
            try:
                statement = select(User).where(User.username == username)
                return session.exec(statement).one()
            except NoResultFound:
                raise NotFoundError(message="User not found")

    def create_user(self, username: str, password: str, email: Optional[str]) -> User:
        hashed_password = self.auth_adapter.get_password_hash(password)
        user = User(username=username, password=hashed_password, email=email)

        try:
            commit(user)
        except IntegrityError:
            raise AlreadyExistsError(message="User already exists")

        return user
