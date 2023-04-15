from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from config.env import pg_username, pg_password, db_uri, db_port, db_name

engine = create_engine(f'postgresql://{pg_username}:{pg_password}@{db_uri}:{db_port}/{db_name}')


class Base(DeclarativeBase):
    pass

