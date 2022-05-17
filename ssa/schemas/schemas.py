from __future__ import annotations

from typing import List, Union, Optional
from pydantic import BaseModel, EmailStr

import datetime




# Users schemas from here.

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
    




# Categories schemes from here.

class CategoryCreate(BaseModel):
    """
    Schema used to create a new Category
    """
    name : str 
    desc : Union[str, None] = None


class CategoryBasic(BaseModel):
    """
    Schema used to provide a basic representation of a Category
    """
    id : int 
    name : str 
    desc : Union[str, None] = None 

    class Config:
        orm_mode = True


class Category(BaseModel):
    """
    Schema generally used to represent a Category
    """
    id : int 
    name : str 
    desc : Union[str, None] = None
    algorithms : List[AlgorithmBasic] = []

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    """
    Schema passed to update a category
    """
    name : Optional[str] = None 
    desc : Optional[str] = None





# Algorithms schemas from here.

class AlgorithmCreate(BaseModel):
    """
    Schema passed to create a new Algorithm
    """
    name : str 
    cost : int 
    desc : Union[str, None] = None
    readme : Union[str, None] = None
    category_id : int 
    author_id : int 
    category : CategoryBasic 
    author : UserBasic


class AlgorithmBasic(BaseModel):
    """
    Schema used for the basic representation of an Algorithm 
    """
    id : int 
    name : str 
    cost : int
    desc : Union[str, None] = None 
    category_id : int 
    author_id : int 


class Algorithm(BaseModel):
    """
    Schema used for the usual representation of an Algorithm
    """
    id : int 
    name : str 
    cost : float 
    desc : Union[str, None] = None
    readme : Union[str, None] = None
    category_id : int 
    author_id : int 
    author : UserBasic 
    calls : List[CallBasic]

    class Config:
        orm_mode = True




# Calls schemes from here.

class CallCreate(BaseModel):
    """
    Schema passed to create a new Call
    """
    datetime : datetime.datetime 
    success : bool 
    user_id : int 
    algorithm_id : int 


class CallBasic(BaseModel):
    """
    Scehma used for the basic representation of a Call
    """
    id : int 
    datetime : datetime.datetime 
    success : bool 
    user_id : int 
    algorithm_id : int 


class Call(BaseModel):
    """
    Schema used for the detailed representation of Call
    """
    id : int 
    datetime : datetime.datetime 
    success : bool 
    user_id : int 
    algorithm_id : int 
    user : UserBasic 
    algorithm : AlgorithmBasic

    class Config:
        orm_mode = True


# Forward refs 
User.update_forward_refs()