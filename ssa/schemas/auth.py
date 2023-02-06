from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    """ Schema passed to login and get a jwt token """
    email : EmailStr 
    password : str 
