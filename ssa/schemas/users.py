from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union 

from .calls import CallBasic
from .algorithms import AlgorithmBasic



class UserCreate(BaseModel):
    """
    Schema passed to the api to create a new User
    """
    email : EmailStr 
    password : str 
    amount : int = 0


class UserBasic(BaseModel):
    """
    Schema returned when only basic information is needed
    """
    id : int 
    email : EmailStr

    class Config:
        orm_mode = True 



class User(BaseModel):
    """
    Schema generally returned to describe a User
    """
    id : int 
    email : EmailStr 
    calls : List[CallBasic] = []
    algorithms : List[AlgorithmBasic] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """
    Schema used to update a user email, password, or amount
    """
    email : Optional[EmailStr] = None
    password : Optional[str] = None
    amount : Optional[int] = None


class UserGetKey(BaseModel):
    """
    Schema returned when a user key is required
    """
    email : EmailStr
    personal_key : str

    class Config:
        orm_mode = True


class UserAskKey(BaseModel):
    """
    Schema to pass to get a user personal key
    """
    email : EmailStr
    password : str