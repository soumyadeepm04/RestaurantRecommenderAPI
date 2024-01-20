from pydantic import BaseModel

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str

class SignInUser(BaseModel):
    username: str
    password: str

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    city: str

class Restaurants:
    def __init__(self, name, latitude, longitude, address, web_url):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.web_url = web_url