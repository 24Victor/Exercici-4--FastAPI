from typing import Union

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

#Array
usuaris_db = []

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    nom: str
    cognom: str
    edat: int
    email: EmailStr

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add_user")
def add_user(user: User):
    usuaris_db.append(user)
    return{"Missatge": "Usuari agregat correctament", "user": user}

@app.get("/users/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": usuaris_db})

@app.get("/user/{user_id}")
async def read_user_detail(user_id: int, request: Request):
    if user_id >= len(usuaris_db):
        return {"error": "Usuari no trobat"}
    
    user = usuaris_db[user_id]
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})

@app.put("/user/{user_id}")
def update_user(user_id: int, user: User):
    usuaris_db[user_id] = user
    return {"Missatge": "Usuari actualitzat correctament", "user": user}