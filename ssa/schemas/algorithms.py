from pydantic import BaseModel, EmailStr
from typing import Union, List, Optional

from .calls import CallBasic
from .categories import CategoryBasic


class AlgorithmCreate(BaseModel):
    """
    Schema passed to create a new Algorithm
    """
    name : str 
    cost : float
    desc : Union[str, None] = None
    readme : Union[str, None] = None
    category_id : int 
    author_id : int
    personal_key : str  


class AlgorithmBasic(BaseModel):
    """
    Schema used for the basic representation of an Algorithm 
    """
    id : int 
    name : str 
    cost : float
    desc : Union[str, None] = None 
    category_id : int 
    author_id : int 

    class Config:
        orm_mode = True


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
    category : CategoryBasic
    calls : List[CallBasic]

    class Config:
        orm_mode = True



class AlgorithmDelete(BaseModel):
    """
    Schema passed to delete an algorithm.
    NOTE: Only who knows the personal key of the author can delete it.
    """
    email : EmailStr 
    personal_key : str 
    name : str 



class AlgorithmUpdate(BaseModel):
    """
    Schema passed to update an Algorithm
    """
    name : Optional[str] = None 
    cost : Optional[float] = None 
    desc : Optional[str] = None 
    readme : Optional[str] = None 
    category_id : Optional[int] = None  