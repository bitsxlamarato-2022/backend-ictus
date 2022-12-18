from fastapi import FastAPI

from models import *

import matplotlib.pyplot as plt
import pandas as pd
import json
import requests
import scipy.io as io

import requests

CLIENT_ID = '238RX8'
CLIENT_SECRET = 'dff37bf9cb0059dfc910129162e035ba'
HOST = "https://api.fitbit.com"


app = FastAPI()

origins = [
    "*"
]


users = {}


@app.post("/register/")
async def register(user: User):
    users[user.id] = user
    return user



@app.post("/login/")
async def login(credentials: Credentials):
    if credentials.id not in users.keys():
        return False
    if users[credentials.id].password != credentials.password:
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
    return users[userid]

def turn_resp_to_mat(resp):
    ys = json.loads(resp.text)['ecgReadings'][0]['waveformSamples']
    dic = {'val': ys}
    io.savemat('tmp.mat', dic)

@app.post("/ecg/{userid}/")
async def get_ecg(userid):
    resp = requests.get(f"{HOST}/1/user/-/ecg/list.json?beforeDate=2022-09-28&sort=asc&limit=10&offset=0", headers={
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzkyM0siLCJzdWIiOiJCM0tZSEgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd2VjZyB3c29jIHdhY3Qgd294eSB3dGVtIHd3ZWkgd2NmIHdzZXQgd2xvYyB3cmVzIiwiZXhwIjoxNjcxMzUxMTQzLCJpYXQiOjE2NzEzMjIzNDN9.cW6yh70CjhJX1RATtssz1u2YAIoNNbKXCiyTC2jHJ3I"
    })
    turn_resp_to_mat(resp)
    return 0
