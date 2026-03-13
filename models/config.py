
from sqlalchemy import Column, String, Text
from .base import Base

class Config(Base):
    __tablename__ = "config"

    key = Column(String, primary_key=True, index=True)
    value = Column(Text)
