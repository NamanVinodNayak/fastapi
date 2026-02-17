from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
    
my_storage = [{"title": "title of post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1},
              {"title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4, "id": 2}]


@app.get("/posts")
async def root():
    return {"message": my_storage}

@app.post("/posts")
def create_post(new_post: Post):
    new_post_dict = new_post.dict()
    new_post_dict['id'] = len(my_storage) + 1
    my_storage.append(new_post_dict)
    return  {"data": new_post_dict}