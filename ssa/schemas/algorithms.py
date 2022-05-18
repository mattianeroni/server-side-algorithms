from pydantic import BaseModel 
from typing import Union, List, Optional

from .calls import CallBasic
from .categories import CategoryBasic


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
    category : CategoryBasic
    calls : List[CallBasic]

    class Config:
        orm_mode = True



class AlgorithmUpdate(BaseModel):
    """
    Schema passed to update an Algorithm
    """
    name : Optional[str] = None 
    cost : Optional[float] = None 
    desc : Optional[str] = None 
    readme : Optional[str] = None 
    category_id : Optional[int] = None  