from fastapi import FastAPI, HTTPException

app =  FastAPI()

@app.get('/')
def greet():
    return {"Hello World"}

users = {}

@app.get("/users/{user_id}")
def get_users(user_id: int):
    return {"user-id": user_id}

@app.post("/user/{user_id}")
def cerate_user(user_id:int, name: str):
    users[user_id] = name
    return {"id":user_id, "name": name}

@app.post("/user/{user_id}")
def replace_user(user_id:int, name: str):
    users[user_id] = name
    return {"id":user_id, "name": name}

@app.patch("/user/{user_id}")
def update_user(user_id:int, name: str):
    users[user_id] = name
    return {"id":user_id, "name": name}

@app.delete("/user/{user_id}")
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user not found")
    del users[user_id]
    return {"message": "user deleted"}
