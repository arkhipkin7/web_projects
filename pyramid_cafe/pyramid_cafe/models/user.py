import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    password = Column(Unicode(255), nullable=False)
    status = Column(Text, nullable=False)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password is not None:
            _hash = self.password.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), _hash)
        return False
