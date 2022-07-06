from pydantic import BaseModel
from typing import List, Optional, Union 


class Transaction (BaseModel):
    """ Schema of a transaction """
    id : int
    user_id : int 
    amount : float

    class Config:
        orm_mode = True
