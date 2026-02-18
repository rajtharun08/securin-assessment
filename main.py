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
def comparison_helper(query, column, value):
    if not value:
        return query
    for operator, operation in OPERATORS.items():
        if value.startswith(operator):
            i=len(operator)
            val = float(value[i:])
            return query.filter(getattr(column, operation)(val))
    return query.filter(column == float(value))

@app.get("/")
def helloworld():
    return {"recipe":"helloworld"}

@app.get("/recipes")
def get_recipes(page: int = 1, limit: int = 10, db: Session = Depends(get_database)):
    step=limit*(page-1)
    query= db.query(tables.Recipe).order_by(desc(tables.Recipe.rating))
    t_count=query.count()
    data=query.offset(step).limit(limit).all()
    return {
        "page":page,
        "limit":limit,
        "total":t_count,
        "data":data
    }

@app.get("/recipes/search")
def search_recipe(title: str = None,cuisine: str = None,calories: str = None,total_time: str = None,rating: str = None,db: Session = Depends(get_database)):
    query = db.query(tables.Recipe)
    if title:
        query = query.filter(tables.Recipe.title.contains(title))
    if cuisine:
        query = query.filter(tables.Recipe.cuisine == cuisine)

    query = comparison_helper(query, tables.Recipe.total_time, total_time)
    query = comparison_helper(query, tables.Recipe.rating, rating)
    
    results = query.all()
    if calories:
        filtered = []
        target_str = calories.replace(">=","").replace("<=","").replace(">","").replace("<","")
        target_val = float(target_str)
        for r in results:
            try:
                nut_str = str(r.nutrients)
                val_part = nut_str.split("'calories': '")[1].split(" ")[0]
                actual_cal = float(val_part)
                if ">=" in calories and actual_cal >= target_val: filtered.append(r)
                elif "<=" in calories and actual_cal <= target_val: filtered.append(r)
                elif ">" in calories and actual_cal > target_val: filtered.append(r)
                elif "<" in calories and actual_cal < target_val: filtered.append(r)
                elif actual_cal == target_val: filtered.append(r)
            except:
                continue 
        return {"data": filtered}
    return {"data": results}
