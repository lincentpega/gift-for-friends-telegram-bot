from typing import Optional, Type

from sqlalchemy import Boolean
from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session

from db_base import Base, engine


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
