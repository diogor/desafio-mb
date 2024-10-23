from sqlmodel import SQLModel, create_engine, Session
from app.settings import DATABASE_URL
from .auth import User

__all__ = ["User"]

engine = create_engine(DATABASE_URL)


def commit(object: SQLModel):
    with Session(engine) as session:
        session.add(object)
        session.commit()
        session.refresh(object)
