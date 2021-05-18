from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
)
from sqlalchemy.orm import relationship
from .meta import Base
from .temp_product import TempProduct


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    data = Column(DateTime)
    product = relationship("TempProduct", backref="products", uselist=False)
