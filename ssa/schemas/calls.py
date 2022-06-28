import datetime 
from pydantic import BaseModel, EmailStr


class CallCreate(BaseModel):
    """ Schema passed to create a new Call """
    token : str 
    algorithm_id : int 
    success : bool = False


class Call(BaseModel):
    """ Schema used for the detailed representation of Call """
    id : int 
    datetime : datetime.datetime 
    success : bool 
    user_id : int 
    algorithm_id : int 

    class Config:
        orm_mode = True