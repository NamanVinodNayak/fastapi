from fastapi import Body, FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import model
from .database import engine, SessionLocal, get_db

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/sqlalchemy")
def root(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"all_posts": posts}

