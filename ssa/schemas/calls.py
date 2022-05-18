import datetime 
from pydantic import BaseModel 


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

    class Config:
        orm_mode = True