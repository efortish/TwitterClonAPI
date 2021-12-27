#Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json
from fastapi.param_functions import Form

#Pydantic

from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import Field


#FastAPI
from fastapi import FastAPI, status, Body
from pydantic.types import SecretStr


app = FastAPI()

#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field (...)

class Passwords(BaseModel):
    password: str = Field (..., min_length=8, max_length=64)

class User(UserBase):
    first_name: str = Field (
    ...,
    min_length= 1,
    max_length=50
    )
    last_name: str = Field (
    ...,
    min_length= 1,
    max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class tweet(BaseModel):
    tweet_id: UUID = Field (...)
    content: str = Field (
        ...,
        min_length=1,
        max_length=256
    )
    created_at : datetime = Field(default=datetime.now())
    updated_at : Optional[datetime] = Field(default=None)
    by: User = Field(...) 

class UserLogin(UserBase, Passwords):
    pass

class UserRegister(User, Passwords):
    pass
class LoginOut(BaseModel): 
    email: EmailStr = Field(...)
    message: str = Field(default=None)

#Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary= "Register a User",
    tags= ["Users"]
)
def signup(user: UserRegister = Body(...) ):
    """
    Signup

    This path operation register a user in the app

    Parameters:
    - Request body parameter:
        - user: UserRegister

    Returns a JSON with basic user's information:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: str
    """
    with open ("users.json", "r+", encoding="utf-8") as f:
        results:list = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


### Login a user
@app.post(
    path="/login",
    response_model= LoginOut,
    status_code= status.HTTP_200_OK,
    summary= "Login a User",
    tags= ["Users"]
)
def login(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    """
    Login a user

    This path Operations login a user in the app based on users.json file wich contains user's data,
    it also verifies if the information is the same to do a login succesfully 

    Parameters:
    - Request Body parameter:
        - email : EmailStr
        - password: str
    
    Returns a message "Done!" if the authentication is ok, or returns "Unsuccesfully authentication!" if it has no coincidence

    """
    with open("users.json", "r+", encoding="utf-8") as f: 
        datos = list(json.loads(f.read()))
        for user in datos:
            if email == user["email"] and password == user["password"]:
                return LoginOut(email=email, message="Done!")
        
        return LoginOut(email=email, message= "Unsuccesfully authentication!")
            
            

    

### Show all user
@app.get(
    path="/users",
    response_model= List[User],
    status_code= status.HTTP_200_OK,
    summary= "Show all Users",
    tags= ["Users"]
)
def show_all_users():
    """
    Show all users

    This path operation shows all users registered in the app

    Parameters:
    - None 

    Returns a json list with all users in the app, with the following keys
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: str

    """
    with open ("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary= "Show a User",
    tags= ["Users"]
)
def show_a_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary= "Delete a User",
    tags= ["Users"]
)
def delete_a_user():
    pass

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary= "Update a User",
    tags= ["Users"]
)
def update_a_user():
    pass
    

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model= List[tweet],
    status_code= status.HTTP_200_OK,
    summary= "Show all tweets",
    tags= ["Tweets"]

    )
def home():
    """
    Show all tweets

    This path operation shows all tweets posted in the app

    Parameters:
    - Request Body parameter:
        - tweet: tweet

    Returns a json file with all tweets in the app, with following keys
    - tweet_id: UUID
    - content: str 
    - created_at : datetime 
    - updated_at : Optional[datetime] 
    - by: User

    """
    with open ("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a Tweet
@app.post(
    path="/post",
    response_model= tweet,
    status_code= status.HTTP_201_CREATED,
    summary= "Post a Tweet",
    tags= ["Tweets"]
)
def post_a_tweet(tweet: tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a tweet in the app

    Parameters:
    - Request body parameter:
        - tweet: Tweet

    Returns a JSON with basic tweet information:
    - tweet_id: UUID
    - content: str 
    - created_at : datetime 
    - updated_at : Optional[datetime] 
    - by: User
    """
    with open ("tweets.json", "r+", encoding="utf-8") as f:
        results:list = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str (tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str (tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a Tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model= tweet,
    status_code= status.HTTP_200_OK,
    summary= "Show a Tweet",
    tags= ["Tweets"]
)
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= tweet,
    status_code= status.HTTP_200_OK,
    summary= "Delete a Tweet",
    tags= ["Tweets"]
)
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= tweet,
    status_code= status.HTTP_200_OK,
    summary= "Update a Tweet",
    tags= ["Tweets"]
)
def Update_a_tweet():
    pass




