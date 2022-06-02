from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union 

from .calls import Call
from .algorithms import AlgorithmBasic



class UserCreate(BaseModel):
    """
    Schema passed to the api to create a new User
    """
    email : EmailStr 
    password : str 
    amount : float = 0.0


class UserBasic(BaseModel):
    """
    Schema returned when only basic information is needed
    """
    id : int 
    email : EmailStr
    personal_key : str

    class Config:
        orm_mode = True 



class User(BaseModel):
    """
    Schema generally returned to describe a User
    """
    id : int 
    email : EmailStr 
    calls : List[Call] = []
    algorithms : List[AlgorithmBasic] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """
    Schema used to update a user email, password, or amount
    """
    email : Optional[EmailStr] = None
    password : Optional[str] = None
    amount : Optional[float] = None



class UserGetKey(BaseModel):
    """
    Schema to pass to get a new personal key
    """
    email : EmailStr
    password : str


class UserWithKey(BaseModel):
    """
    Schema like UserBasic but it returns the personal key as well
    """
    id : int 
    email : EmailStr
    personal_key : str

    class Config:
        orm_mode = True 


class UserDelete(BaseModel):
    """
    Schema to delete a user
    """
    email : EmailStr 
    password : str 