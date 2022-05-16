from  __future__ import annotations
from typing import List, Union, Optional
import datetime

from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    email : EmailStr 
    password : str 
    amount : int


class User(BaseModel):
    id : int 
    email : EmailStr 
    calls : List[Call] = []
    algorithms : List[Algorithm] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email : Optional[EmailStr] = None
    password : Optional[str] = None
    amount : Optional[int] = None


class UserKey(BaseModel):
    email : EmailStr
    personal_key : str

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name : str 
    desc : Union[str, None] = None


class Category(BaseModel):
    id : int 
    name : str 
    desc : Union[str, None] = None
    algorithms : List[Algorithm] = []

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    name : Optional[str] = None 
    desc : Optional[str] = None



class AlgorithmCreate(BaseModel):
    name : str 
    cost : int 
    desc : Union[str, None] = None
    readme : Union[str, None] = None
    category_id : int 
    author_id : int 


class Algorithm(BaseModel):
    id : int 
    name : str 
    cost : float 
    desc : Union[str, None] = None
    readme : Union[str, None] = None
    category_id : int 
    author_id : int 
    category : Category 
    author : User 
    calls : List[Call] = []

    class Config:
        orm_mode = True


class CallCreate(BaseModel):
    datetime : datetime.datetime 
    success : bool 
    user_id : int 
    algorithm_id : int 


class Call(BaseModel):
    id : int 
    datetime : datetime.datetime 
    success : bool 
    user_id : int 
    algorithm_id : int 
    user : User 
    algorithm : Algorithm

    class Config:
        orm_mode = True
        