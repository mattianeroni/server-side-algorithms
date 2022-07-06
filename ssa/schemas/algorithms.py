from pydantic import BaseModel, EmailStr
from typing import Union, List, Optional
from fastapi import File, UploadFile

from .calls import Call
from .categories import CategoryBasic


class AlgorithmCreate(BaseModel):
    """ Schema passed to create a new Algorithm """
    token : str 
    name : str 
    cost : float
    desc : Union[str, None] = None
    category_id : int 


class AlgorithmBasic(BaseModel):
    """ Schema used for the basic representation of an Algorithm """
    id : int 
    name : str 
    cost : float
    desc : Union[str, None] = None 
    category_id : int 
    author_id : int 
    trusted : bool

    class Config:
        orm_mode = True


class Algorithm(BaseModel):
    """ Schema used for the usual representation of an Algorithm """
    id : int 
    name : str 
    cost : float 
    desc : Union[str, None] = None
    trusted : bool 
    category_id : int
    author_id : int 
    category : CategoryBasic
    calls : List[Call]

    class Config:
        orm_mode = True



class AlgorithmDelete(BaseModel):
    """ Schema passed to delete an algorithm """
    id : int
    token : str  


class AlgorithmUpdate(BaseModel):
    """ Schema passed to update an Algorithm """
    id : int 
    token : str 
    name : Optional[str] = None 
    cost : Optional[float] = None 
    desc : Optional[str] = None  
    category_id : Optional[int] = None  


class AlgorithmValidate(BaseModel):
    """ Schema used by the admin to validate an algorithm """ 
    id : int 
    token : str 