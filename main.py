#Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json


#Pydantic

from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import Field


#FastAPI
from fastapi import FastAPI, status, Body
from pydantic.types import SecretStr
from fastapi import HTTPException
from fastapi.param_functions import Form, Path


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

class DeleteUser(BaseModel):
    user_id: UUID = Field (...)
    message: str = Field (default= "User Deleted")


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
def signup(
    user: UserRegister = Body(...) 
):
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
    
    Returns a message "Done!" if the authentication is ok, or returns "Unsuccesfully authentication!" if it has no coincidence, both cases returns the user's email as a response

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
def show_a_user(
    user_id: str = Path (
    ...,
    min_length=1,
    example= "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
):
    """
    Show a user by ID

    This path operation shows a user by ID

    Parameters:
    - Request body parameter:
        - **user_id**: str 
    
    Returns a json with the user's information: first_name, last_name, email, user_id, date_of_birth
    
    """

    with open ("users.json", "r", encoding="utf-8") as f:
        results = list(json.loads(f.read()))
        for user in results:
            if user_id == user["user_id"]:
                user = dict(user)
                return user
        
        if user_id != user["user_id"]:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "This user does not exist!")
                   
            
    

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model= DeleteUser,
    status_code= status.HTTP_202_ACCEPTED,
    summary= "Delete a User",
    tags= ["Users"]
)
def delete_a_user(
    user_id: str = Path(
        ...
        
    )
):

    """
    Delete a user

    This path operation deletes a user 

    Parameters:
    - Request Body Parameters:
        - user_id: str
    
    Returns a json saying the user provided was succesfully deleted, if the user does not exists, the json will show it up to you
    
    
    
    """

    with open ("users.json", "r+", encoding="utf-8") as f:
        results = list(json.loads(f.read()))
        for user in results:
            if user["user_id"] == user_id:
                results.remove(user)
                with open("users.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return user
    if 1==1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user_id doesn't exist!"
        )
            
                
            
    

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary= "Update a User",
    tags= ["Users"]
)
def update_a_user(
    user_id: UUID = Path(...),
    user: User = Body (...)
):  

    """
    Update a User

    This path operation updates user's information, even the user ID

    Parameters:
    - Response Body parameters:
        - user_id: UUID -> user's id
        - user: User -> User object wich contains first_name, last_name, date_of_birth, used_id and email

    Returns a Json with User Json information with the new data given, sometimes its necesary do the execute twice to work  
    
    """
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    
    with open("users.json", "r+", encoding="utf-8") as f: 
        results = list(json.loads(f.read()))
        for user in results:
            if user["user_id"] == user_id:
                results[results.index(user)] = user_dict
                with open("users.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return user
    

    
    
    

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
def show_a_tweet(tweet_id:str=Path(...)):
    """
    Show a tweet by ID

    This path operation shows a tweet by ID

    Parameters:
    - Request body parameter:
        - **user_id**: str 
    
    Returns a json with the user's information: first_name, last_name, email, user_id, date_of_birth
    
    """

    with open ("tweets.json", "r+", encoding="utf-8") as f:
        # tweet_dict = dict(tweet_id)
        # tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        # tweet_dict["created_at"] = str(tweet_dict["created_at"])
        # tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        # tweet_dict["by"]["user_id"] = str (tweet_dict["by"]["user_id"])
        # tweet_dict["by"]["birth_date"] = str (tweet_dict["by"]["birth_date"])
        results = list(json.loads(f.read()))
        for tw in results:
            if tw["tweet_id"] == tweet_id:
                tw = dict(tw)
                return tw
        
        if tw["tweet_id"] != tweet_id:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "This tweet does not exist!")

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= tweet,
    status_code= status.HTTP_200_OK,
    summary= "Delete a Tweet",
    tags= ["Tweets"]
)
def delete_a_tweet(tweet_id:str=Path(...)):
    """
    Delete a tweet

    This path operation deletes a tweet 

    Parameters:
    - Request Body Parameters:
        - tweet_id: str
    
    Returns a json saying the tweet provided was succesfully deleted, if the user does not exists, the json will show it up to you
    
    
    
    """

    with open ("tweets.json", "r+", encoding="utf-8") as f:
        results = list(json.loads(f.read()))
        for tweet in results:
            if tweet["tweet_id"] == tweet_id:
                results.remove(tweet)
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return tweet
    if 1==1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet doesn't exist!"
        )
    

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= tweet,
    status_code= status.HTTP_200_OK,
    summary= "Update a Tweet",
    tags= ["Tweets"]
)
def Update_a_tweet(
    tweet_id:str=Path(...), 
    tweet:tweet=Body(...)
    ):
    """
    Update a Tweet

    This path operation updates tweet's information, even the user ID

    Parameters:
    - Response Body parameters:
        - tweet_id: str -> Tweet's ID 
        - tweet: tweet -> tweet object wich contains first_name, last_name, date_of_birth, used_id and email

    Returns a Json with User Json information with the new data given, sometimes its necesary do the execute twice to work  
    
    """
    tweet_id = str(tweet_id)
    tweet_dict = tweet.dict()
    tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    tweet_dict["created_at"] = str(tweet_dict["created_at"])
    tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
    tweet_dict["by"]["user_id"] = str (tweet_dict["by"]["user_id"])
    tweet_dict["by"]["birth_date"] = str (tweet_dict["by"]["birth_date"])
    
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = list(json.loads(f.read()))
        for tweet in results:
            if tweet["tweet_id"] == tweet_id:
                results[results.index(tweet)] = tweet_dict
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return tweet




