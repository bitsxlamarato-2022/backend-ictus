
from pydantic import BaseModel

from xmlrpc.client import Boolean


class User(BaseModel):
    id: str
    passwrd: str
    name: str
    surname: str
    age: int
    weight: int
    height: int