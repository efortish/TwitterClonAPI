#Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

#Pydantic

from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import Field


#FastAPI
from fastapi import FastAPI, status


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

class UserRegister(UserBase, Passwords):
    pass


#Path Operations

@app.get(path="/")
def home():
    return {
        "Twitter API": "Working!"
    }

## Users

### Register a user
@app.post(
    path="/signup",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary= "Register a User",
    tags= ["Users"]
)
def signup():
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

### Login a user
@app.post(
    path="/login",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary= "Login a User",
    tags= ["Users"]
)
def login():
    pass

### Show all user
@app.get(
    path="/users",
    response_model= List[User],
    status_code= status.HTTP_200_OK,
    summary= "Show all Users",
    tags= ["Users"]
)
def show_all_users():
    pass

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
    return {
        "Twitter API": "Working!"
    }

### Post a Tweet
@app.post(
    path="/post",
    response_model= tweet,
    status_code= status.HTTP_201_CREATED,
    summary= "Post a Tweet",
    tags= ["Tweets"]
)
def post_a_tweet():
    pass

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




