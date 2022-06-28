from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union 

from .calls import Call
from .algorithms import AlgorithmBasic



class UserCreate(BaseModel):
    """ Schema passed to the api to create a new User """
    email : EmailStr 
    password : str 
    amount : float = 0.0


class UserBasic(BaseModel):
    """ Schema returned when only basic information is needed """
    id : int 
    email : EmailStr
    role : int 
    amount : float

    class Config:
        orm_mode = True 



class User(BaseModel):
    """ Schema generally returned to describe a User """
    id : int 
    email : EmailStr 
    role : int
    amount : float
    calls : List[Call] = []
    algorithms : List[AlgorithmBasic] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """ Schema used to update a user email or password """
    token : str 
    email : Optional[EmailStr] = None
    password : Optional[str] = None


class UserDelete(BaseModel):
    """ Schema to delete a user """
    token : str


class UserUpdateAmount(BaseModel):
    """ Schema to update a user amount """ 
    token : str 
    amount : float 
    user_id : int 