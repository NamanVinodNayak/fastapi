from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def root():
    return {"message": "This is the posts page"}

@app.post("/new_posts")
def create_post(payload: dict = Body(...)):
    return  {
            "message": "Post created successfully", 
            "payload": payload,
            "content": "good",
            "status": "success",
            "payload_title" : f"{payload['title']}",
            "payload_content" : f"{payload['content']}"
             }