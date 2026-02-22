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

class Post_py(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/sqlalchemy")
def root(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"all_posts": posts}

@app.post("/sqlalchemy", status_code=status.HTTP_201_CREATED)
def create_post(post:Post_py, db: Session = Depends(get_db)):
    #new_post = model.Post(title=post.title, content=post.content, published=post.published)
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/sqlalchemy/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post_one = db.query(model.Post).filter(model.Post.id_post == id).first()
    if not post_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return {"post_detail": post_one }