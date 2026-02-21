from typing import Optional
from fastapi import Body, FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import psycopg2

app = FastAPI()

# we will use pydantic to validate the data that we receive from the client
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
try:
    conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password123")
    cursor = conn.cursor()
    print("\n********************************************\nDatabase connection successful\n********************************************\n")

except Exception as error:
    print("Database connection failed")
    print(error)
    
#without database, we will use a list to store our posts
my_storage = [{"title": "title of post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1, "created_at": datetime.now()},
              {"title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4, "id": 2, "created_at": datetime.now()}]

# retrive one post function
def find_post(id):
    for post in my_storage:
        if post['id'] == id:
            return post

# retrive all posts
@app.get("/posts")
def root():
    return {"message": my_storage}

# retrive one post
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return {"data": post}

# create a new post and add it to the storage list, we will use the pydantic model to validate the data that we receive from the client
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    new_post_dict = new_post.dict()
    new_post_dict['id'] = len(my_storage) + 1
    my_storage.append(new_post_dict)
    return  {"data": new_post_dict}

# delete a post by id, if the post does not exist, we will return a 404 error
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    my_storage.remove(post)
    return {"message": f"Post with id {id} has been deleted"}

# update a post by id, if the post does not exist, we will return a 404 error
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    post_index = my_storage.index(post)
    updated_post_dict = updated_post.dict()
    updated_post_dict['id'] = id
    my_storage[post_index] = updated_post_dict
    return {"data": updated_post_dict}


