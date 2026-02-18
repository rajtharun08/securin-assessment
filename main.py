from fastapi import FastAPI,Depends,Query
from sqlalchemy.orm import Session
from typing import List, Optional
import tables;
from database import engine, get_database

app=FastAPI()
tables.Base.metadata.create_all(bind=engine)

@app.get("/recipes/search")
def search_recipes(title: Optional[str] = None,cuisine: Optional[str] = None,db: Session = Depends(get_database)):
    query = db.query(tables.Recipe)
    if title:
        query = query.filter(tables.Recipe.title.contains(title))
    if cuisine:
        query = query.filter(tables.Recipe.cuisine == cuisine)
    return query.all()
