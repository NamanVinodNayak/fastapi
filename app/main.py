from typing import Optional
from fastapi import Body, FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# we will use pydantic to validate the data that we receive from the client
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
try:
    conn = psycopg2.connect(
    host="localhost",
    database="fastapi",
    user="postgres",
    password="password123",
    cursor_factory=RealDictCursor
)
    cursor = conn.cursor()
    print("\n🔰🔰🔰🔰🔰🔰🔰🔰🔰")
    print("********************************************\nDatabase connection successful\n********************************************\n")

except Exception as error:
    print("🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨")
    print("Database connection failed")
    print(error)
    time.sleep(5)
  
# retrive one post function
def find_post(id):
    for post in my_storage:
        if post['id'] == id:
            return post

# retrive all posts
@app.get("/posts")
def root():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts

# retrive one post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id_post = %s""",(str(id),))
    post_one = cursor.fetchone()
    if not post_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return {"post_detail": post_one }

# create a new post, we will return the created post with a 201 status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute(
        """
        INSERT INTO posts (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *
        """,
    (new_post.title, new_post.content, new_post.published))
    conn.commit()
    created_post = cursor.fetchone()
    return created_post

# delete a post by id, if the post does not exist, we will return a 404 error
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id_post=%s RETURNING *""",(str(id),))
    conn.commit()
    del_post = cursor.fetchone()
    
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return del_post

# update a post by id, if the post does not exist, we will return a 404 error
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id_post=%s RETURNING *""",(updated_post.title,updated_post.content,updated_post.published,str(id)))
    conn.commit()
    new_update_post = cursor.fetchone()
    if not new_update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return {"data": new_update_post}


