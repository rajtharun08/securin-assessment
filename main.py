from fastapi import FastAPI,Depends,Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
import tables;
from database import engine, get_database

app=FastAPI()
tables.Base.metadata.create_all(bind=engine)

OPERATORS = {
    ">=":"__ge__",
    "<=":"__le__",
    ">":"__gt__",
    "<": "__lt__"
}

@app.get("/")
def helloworld():
    return {"recipe":"helloworld"}

@app.get("/recipes")
def get_paginated_recipes(page: int = 1, limit: int = 10, db: Session = Depends(get_database)):
    step=limit*(page-1)
    
    data = db.query(tables.Recipe).order_by(desc(tables.Recipe.rating)).offset(step).limit(limit).all()
    return data

