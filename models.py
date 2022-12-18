
from pydantic import BaseModel

from xmlrpc.client import Boolean


class User(BaseModel):
    id: str
    password: str
    name: str
    surname: str
    age: int
    weight: int = 0
    height: int = 0 

class Credentials(BaseModel):
    id: str
    password: str