from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    ForeignKey,
)
from .meta import Base


class TempProduct(Base):
    __tablename__ = 'temp_products'
    id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    data = Column(DateTime)
