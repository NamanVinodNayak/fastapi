from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
#without database, we will use a list to store our posts
my_storage = [{"title": "title of post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1},
              {"title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4, "id": 2}]

# retrive one post
def find_post(id):
    for post in my_storage:
        if post['id'] == id:
            return post


@app.get("/posts")
async def root():
    return {"message": my_storage}

@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        return {"message": f"Post with id {id} does not exist"}
    return {"data": post}

@app.post("/posts")
def create_post(new_post: Post):
    new_post_dict = new_post.dict()
    new_post_dict['id'] = len(my_storage) + 1
    my_storage.append(new_post_dict)
    return  {"data": new_post_dict}