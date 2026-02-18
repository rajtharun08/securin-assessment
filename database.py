from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker , declarative_base
from urllib.parse import quote_plus

password = quote_plus("Tharun@08")

url="mysql+pymysql://root:{password}@localhost:3306/recipe_db"
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_database():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()