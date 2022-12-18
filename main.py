from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from models import *

import matplotlib.pyplot as plt
import pandas as pd
import json
import requests
import scipy.io as sciio
import io

import requests

CLIENT_ID = '23923K'
CLIENT_SECRET = 'e75bf5bf8e57aac3689717bad636cb97'
HOST = "https://api.fitbit.com"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzkyM0siLCJzdWIiOiJCM0tZSEgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd2VjZyB3c29jIHdhY3Qgd294eSB3dGVtIHd3ZWkgd2NmIHdzZXQgd3JlcyB3bG9jIiwiZXhwIjoxNjcxMzgyMDExLCJpYXQiOjE2NzEzNTMyMTF9.raqNgqDxyvXOmRc1z3hZsGFE31XGc_Te0OArTYoqVzg"

app = FastAPI()

origins = [
    "*"
]

users = {"string": User(id="string", password="pollagorda69", name="pol", surname="escolar", age=12)}


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
    sciio.savemat('tmp.mat', dic)


@app.post("/ecg/{userid}/")
async def get_ecg(userid):
    resp = requests.get(f"{HOST}/1/user/-/ecg/list.json?beforeDate=2022-09-28&sort=asc&limit=10&offset=0", headers={
        "Authorization": f"Bearer {BEARER_TOKEN}"
    })
    turn_resp_to_mat(resp)
    return 0


def plot_ecg(resp):
    plt.figure()
    ys = json.loads(resp.text)['ecgReadings'][4]['waveformSamples']
    xs = [x for x in range(len(ys))]
    plt.plot(xs, ys)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    print("HA")
    return buf


@app.get("/egs/{userid}/")
async def egs_image(userid: str, ):
    resp = requests.get(f"{HOST}/1/user/-/ecg/list.json?beforeDate=2022-09-28&sort=asc&limit=10&offset=0", headers={
        "Authorization": f"Bearer {BEARER_TOKEN}"
    })
    image_buf = plot_ecg(resp)
    return StreamingResponse(content=image_buf, media_type="image/png")
