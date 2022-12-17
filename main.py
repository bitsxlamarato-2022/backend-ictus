from fastapi import FastAPI

from models import *
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sqlalchemy

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
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


oneDate = pd.datetime(year = 2002, month = 12, day = 16)
oneDayData = auth2_client.intraday_time_series('activities/heart', oneDate, detail_level='1sec')
df= pd.DataFrame(oneDayData['activities-heart-intraday']["dataset"])

print(df)
df.to_csv('HRdata.csv')
""""""

app = FastAPI()

users = {}



@app.post("/register")
async def register(user: User):
    users[user.id] = user
    return user

@app.post("/login")
async def login(user: User):
    if user.id not in users.keys():
        return False
    if users[user].passwrd != user.passwrd:
        return False
    return True

@app.post("/user")
async def edit_user(user: User):
    if user.id not in users.keys():
        return None
    users[user.id] = user
    return users

@app.get("/users/{userid}")
async def get_ecg(userid):
    #get_info()
    return users[userid]