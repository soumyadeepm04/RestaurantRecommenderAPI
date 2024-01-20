import hashlib
import requests
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

cuisine_dict = {"Asian": 0, "International": 1, "Indonesian": 2, "Italian": 3, "Steakhouse": 4, "Cafe": 5, "European": 6, "American": 7, "Barbecue": 8, "Halal": 9, "Wine Bar": 10, "Peruvian": 11, "Japanese Fusion": 12, "Southwestern": 13, "Pub": 14, "Mediterranean": 15, "Chinese": 16, "Seafood": 17}

@app.post("/sign-up/", response_model=schemas.CreateUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code = 400, detail = "Username already exists.")
    crud.create_user(db = db, user = user)
    return user

@app.put("/sign-in/", response_model=str)
def sign_in(user: schemas.SignInUser, db: Session = Depends(get_db)):
    
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code = 400, detail = "Invalid username.")
    
    elif db_user.hashed_password != hashlib.sha256(user.password.encode('UTF-8')).hexdigest():
        raise HTTPException(status_code = 400, detail = "Invalid password")
    return "Successful"

@app.put("/like/", response_model=str)
def like(user: str, cuisines: list[str], db: Session = Depends(get_db)):
    db_user = crud.preferences_user(db, user)

    if not db_user:
        crud.create_user_preferences(db, user)
    for element in cuisines:
        if cuisine_dict[element] is not None:
            if element == "Wine Bar":
                crud.update_preferences_like(db, "Wine_Bar", user)
            elif element == "Japanese Fusion":
                crud.update_preferences_like(db, "Japanese_Fusion", user)
            else:
                crud.update_preferences_like(db, element, user)
        else:
            raise HTTPException(status_code=400, detail = "Invalid cuisine entered")
    return "Successful"

@app.put("/dislike/", response_model=str)
def dislike(user: str, cuisines: list[str], db: Session = Depends(get_db)):
    db_user = crud.preferences_user(db, user)

    if not db_user:
        crud.create_user_preferences(db, user)
    for element in cuisines:
        if cuisine_dict[element] is not None:
            if element == "Wine Bar":
                crud.update_preferences_dislike(db, "Wine_Bar", user)
            elif element == "Japanese Fusion":
                crud.update_preferences_dislike(db, "Japanese_Fusion", user)
            else:
                crud.update_preferences_dislike(db, element, user)
        else:
            raise HTTPException(status_code=400, detail = "Invalid cuisine entered")
    return "Successful"      

@app.get("/preferences/")
def get_preferences(user: str, location: str, db: Session = Depends(get_db)):

    url1 = "https://worldwide-restaurants.p.rapidapi.com/typeahead"

    payload = {
        "q": location,
        "language": "en_US"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
    }

    idRequest = requests.post(url1, data=payload, headers=headers)

    idJson = idRequest.json()

    id = idJson["results"]["data"][0]["result_object"]["location_id"]

    db_user = crud.preferences_user(db, user)

    if not db_user:
        crud.create_user_preferences(db, user)
    
    db_user = crud.preferences_user(db, user)

    url = "https://worldwide-restaurants.p.rapidapi.com/search"

    payload = {
        "language": "en_US",
        "location_id": id,
        "currency": "USD",
        "offset": "0"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    jsonResponse = response.json()

    list = []

    preference_list = []

    for item in jsonResponse["results"]["data"]:
        x = schemas.Restaurants(item.get('name'), item.get('latitude'), item.get('longitude'), item.get('address'), item.get('web_url'))
        list.append(x)

    sum_list = []

    
    inverse_dict = {0: "Asian", 1: "International", 2: "Indonesian", 3: "Italian", 4: "Steakhouse", 5: "Cafe", 6: "European", 7: "American", 8: "Barbecue", 9: "Halal", 10: "Wine Bar", 11: "Peruvian", 12: "Japanese Fusion", 13: "Southwestern", 14: "Pub", 15: "Mediterranean", 16: "Chinese", 17: "Seafood"}
    if len(list) > 0:
        for item in jsonResponse["results"]["data"]:
            temp = [0] * 18
            for element in item["cuisine"]:
                x = cuisine_dict.get(element["name"])
                if x is not None:
                    temp[x] = 1
            sum = 0
            index = 0
            for element in temp:
                if element == 1:
                    if inverse_dict.get(index) == "Wine Bar":
                        sum += getattr(db_user, "Wine_Bar")
                    elif inverse_dict.get(index) == "Japanese Fusion":
                        sum += getattr(db_user, "Japanese_Fusion")
                    else:
                        sum += getattr(db_user, inverse_dict.get(index))
                index = index + 1
            sum_list.append(sum)
        
        index = 0
        while index < len(list):
            max_value = -1
            curr_index = index
            index2 = index

            while index2 < len(sum_list):
                if sum_list[index2] > max_value:
                    max_value = sum_list[index2]
                    curr_index = index2
                index2 = index2 + 1
            
            temp1 = sum_list[index]
            sum_list[index] = sum_list[curr_index]
            sum_list[curr_index] = temp1

            temp2 = list[index]
            list[index] = list[curr_index]
            list[curr_index] = temp2

            index = index + 1
            
        index = 0
        while index < 5 and index < len(list):
            preference_list.append(list[index])
            index = index + 1

    for element in preference_list:
        print(element.name)
    return preference_list