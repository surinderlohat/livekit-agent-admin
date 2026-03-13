
from sqlalchemy import Column, String, Text
from .base import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    description = Column(Text)
    config = Column(Text)
