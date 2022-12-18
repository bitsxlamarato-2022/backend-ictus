from fastapi import FastAPI

from models import *

import pandas as pd

CLIENT_ID = '238RX8'
CLIENT_SECRET = 'dff37bf9cb0059dfc910129162e035ba'
HOST = "https://api.fitbit.com"


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {}

@app.post("/register/")
async def register(user: User):
    users[user.id] = user
    return user

@app.post("/login/")
async def login(user: User):
    if user.id not in users.keys():
        return False
    if users[user].password != user.passwrd:
        return False
    return True

@app.post("/user/")
async def edit_user(user: User):
    if user.id not in users.keys():
        return None
    users[user.id] = user
    return users

@app.get("/users/{userid}/")
async def get_user(userid):
    get_info()
    return users[userid]

    
@app.post("/ecg/{userid}/")
async def get_ecg(userid):
    get_info()
    return users[userid]
