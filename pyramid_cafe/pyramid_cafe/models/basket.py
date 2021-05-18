from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Basket(Base):
    __tablename__ = 'baskets'
    id = Column(Integer, primary_key=True)
    data = Column(Text)
    price = Column(Integer, nullable=False)
    datetime = Column(DateTime)
    qrcode = Column(Text)

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_baskets')
