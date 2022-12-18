from fastapi import FastAPI
from fastapi.responses import Response

from models import *

import matplotlib.pyplot as plt
import pandas as pd
import json
import requests
import scipy.io as io
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sqlalchemy

import fitbit
import gather_keys_oauth2 as Oauth2

import requests

CLIENT_ID = '238RX8'
CLIENT_SECRET = 'dff37bf9cb0059dfc910129162e035ba'
HOST = "https://api.fitbit.com"

CLIENT_ID = '23923K'
CLIENT_SECRET = 'e75bf5bf8e57aac3689717bad636cb97'
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                             refresh_token=REFRESH_TOKEN)
auth2_client.make_request(
    'https://api.fitbit.com/1/user/-/ecg/list.json?beforeDate=2022-09-28&sort=asc&limit=1&offset=0')

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
    io.savemat('tmp.mat', dic)


@app.post("/ecg/{userid}/")
async def get_ecg(userid):
    resp = requests.get(f"{HOST}/1/user/-/ecg/list.json?beforeDate=2022-09-28&sort=asc&limit=10&offset=0", headers={
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzkyM0siLCJzdWIiOiJCM0tZSEgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd2VjZyB3c29jIHdhY3Qgd294eSB3dGVtIHd3ZWkgd2NmIHdzZXQgd2xvYyB3cmVzIiwiZXhwIjoxNjcxMzUxMTQzLCJpYXQiOjE2NzEzMjIzNDN9.cW6yh70CjhJX1RATtssz1u2YAIoNNbKXCiyTC2jHJ3I"
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
    return buf


@app.post("/egs/{userid}/", responses={
    200: {
        "content": {"image/png": {}}
    }
}, response_class=Response
          )
async def egs_image(userid):
    resp = requests.get(f"{HOST}/1/user/-/ecg/list.json?beforeDate=2022-09-28&sort=asc&limit=10&offset=0", headers={
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzkyM0siLCJzdWIiOiJCM0tZSEgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd2VjZyB3c29jIHdhY3Qgd294eSB3dGVtIHd3ZWkgd2NmIHdzZXQgd2xvYyB3cmVzIiwiZXhwIjoxNjcxMzUxMTQzLCJpYXQiOjE2NzEzMjIzNDN9.cW6yh70CjhJX1RATtssz1u2YAIoNNbKXCiyTC2jHJ3I"
    })
    image_buf = plot_ecg(resp)
    return Response(content=image_buf, media_type="image/png")
