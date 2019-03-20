from loguru import logger
from sqla_wrapper import SQLAlchemy
from sqlalchemy import BigInteger, Column, Integer, JSON, String
from sqlalchemy.exc import SQLAlchemyError

from forward import conf
from .utils import db_session_scope

db = SQLAlchemy(conf.db_uri, scopefunc=db_session_scope)


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def get_by_id(cls, model_id):
        try:
            return db.query(cls).get(model_id)
        except SQLAlchemyError:
            logger.exception()
            raise


class Admin(BaseModel):
    admin_id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True)


class WallPost(BaseModel):
    wall_post_id = Column(Integer, primary_key=True)
    text = Column(String)
    data = Column(JSON)

    @property
    def source(self):
        return f'https://vk.com/wall{conf.group_id}_{self.wall_post_id}'

    def __str__(self):
        return f'{self.wall_post_id} - {self.text}'