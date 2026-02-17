from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

my_storage = [
    {"name": "Naman", "age": 26, "roll_no": 1},
    {"name": "Akash", "age": 25, "roll_no": 2}
]

def find_user(roll_no: int):
    return next((u for u in my_storage if u["roll_no"] == roll_no), None)

@app.get("/users")
def get_all_users():
    return my_storage

@app.post("/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    next_id = max(u["roll_no"] for u in my_storage) + 1
    new_user = user.dict()
    new_user["roll_no"] = next_id
    my_storage.append(new_user)
    return new_user

@app.delete("/users/{roll_no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(roll_no: int):
    user = find_user(roll_no)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    my_storage.remove(user)

@app.put("/users/{roll_no}")
def update_user(roll_no: int, new_user: User):
    search_id = find_user(roll_no)
    if not search_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    new_user_index = my_storage.index(search_id)
    new_user_dict = new_user.dict()
    my_storage[new_user_index]=new_user
    return my_storage
    