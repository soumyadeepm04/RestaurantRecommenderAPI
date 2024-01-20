from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Preferences(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key = True, index = True)
    user = Column(String, ForeignKey("users.username"), index=True)
    Asian = Column(Integer, default=0)
    International = Column(Integer, default=0)
    Indonesian = Column(Integer, default=0)
    Italian = Column(Integer, default=0)
    Steakhouse = Column(Integer, default=0)
    Cafe = Column(Integer, default=0)
    European = Column(Integer, default=0)
    American = Column(Integer, default=0)
    Barbecue = Column(Integer, default=0)
    Halal = Column(Integer, default=0)
    Wine_Bar = Column(Integer, default=0)
    Peruvian = Column(Integer, default=0)
    Japanese_Fusion = Column(Integer, default=0)
    Southwestern = Column(Integer, default=0)
    Pub = Column(Integer, default=0)
    Mediterranean = Column(Integer, default=0)
    Chinese = Column(Integer, default=0)
    Seafood = Column(Integer, default=0)