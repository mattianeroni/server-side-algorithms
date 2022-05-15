from typing import List, Union
import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    email : str 
    password : str 
    amount : float 
    parsonal_key : str 


class User(BaseModel):
    id : int 
    email : str 
    calls : List[Call] = []
    algorithms : List[Algorithm] = []

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




class AlgorithmCreate(BaseModel):
    name : str 
    cost : float 
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
