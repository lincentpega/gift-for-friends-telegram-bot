from typing import Optional, Type

from sqlalchemy import BIGINT
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session

from config.db_base import Base, engine


class User(Base):
    __tablename__ = 'account'
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    tried: Mapped[bool] = mapped_column(Boolean)

    def is_tried(self) -> bool:
        return self.tried


def add_user(user: User) -> Type[User]:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        return session.get(User, user.user_id)


def get_user(user_id: int) -> Optional[User]:
    with Session(engine) as session:
        return session.get(User, user_id)


def mark_user_as_tried(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        user.tried = True
        session.commit()
