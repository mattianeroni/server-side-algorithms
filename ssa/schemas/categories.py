from pydantic import BaseModel 
from typing import Union, Optional 


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

    class Config:
        orm_mode = True


class Category(BaseModel):
    """
    Schema generally used to represent a Category
    """
    id : int 
    name : str 
    desc : Union[str, None] = None

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    """
    Schema passed to update a category
    """
    name : Optional[str] = None 
    desc : Optional[str] = None