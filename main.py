from fastapi import FastAPI

from models import *
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sqlalchemy

import requests

import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd

CLIENT_ID = '238RX8'
CLIENT_SECRET = 'dff37bf9cb0059dfc910129162e035ba'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
#from oauthlib.oauth2 import WebApplicationClient
#WebApplicationClient()
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
print(ACCESS_TOKEN)
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


def get_info():
    oneDate = pd.datetime(year = 2022, month = 12, day = 16)
    oneDayData = auth2_client.intraday_time_series('activities/heart', oneDate, detail_level='1sec')
    df= pd.DataFrame(oneDayData['activities-heart-intraday']["dataset"])
    df.to_csv('HRdata.csv')
    #print(df)
    print("HA")
    ecg = requests.get(f"https://api.fitbit.com/1/user/{ACCESS_TOKEN}/ecg/list.json?afterDate=2022-09-28&sort=asc&limit=1&offset=0")
    
    print(ecg)




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
async def get_ecg(userid):
    get_info()
    return users[userid]

    
@app.post("/ecg/{userid}/")
async def get_ecg(userid):
    get_info()
    return users[userid]