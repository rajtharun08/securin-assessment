from sqlalchemy import engine,Column,Integer,String,Float,JSON,Text
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    cuisine = Column(String(100))
    title = Column(String(255))
    rating = Column(Float)
    prep_time = Column(Integer)
    cook_time = Column(Integer)
    total_time = Column(Integer)
    description = Column(Text)
    nutrients = Column(JSON) 
    serves = Column(String(50))