from typing import AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy import update, delete, select, insert

from ssa import schemas, models 
from database import async_session
from templates import templates

import crypt
import jwt
from decouple import config

PRIVATE_KEY = config("PRIVATE_KEY")


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        #async with session.begin():
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()


async def get_templates() -> Jinja2Templates:
    yield templates 


async def verify_user(db: AsyncSession, user_id: int, password: str) -> bool:
    """
    Method used to verify a user by using his / her id.

    :param db: the session.
    :param user_id: the unique id that identifies the user
    :param password: the provided password.
    :return: True if the user is verified, False otherwise.
    """
    query = await db.execute(select(models.User).where(models.User.id == user_id))
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_db.password != crypt.crypt(password, salt=user_db.salt):
        return False
    
    return True


async def verify_user_by_email(db: AsyncSession, email: EmailStr, password: str) -> bool:
    """
    Method used to verify a user by using his / her email.

    :param db: the session.
    :param email: the email of the user.
    :param password: the provided password.
    :return: True if the user is verified, False otherwise.
    """
    query = await db.execute(select(models.User).where(models.User.email == email))
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_db.password != crypt.crypt(password, salt=user_db.salt):
        return False
    
    return True


async def create_token(email: str) -> str:
    """ Method used to create a token with HS256 """
    return jwt.encode({"email": email}, PRIVATE_KEY, algorithm="HS256")



async def verify_token(db: AsyncSession, token : str) -> EmailStr:
    """ Method used to verify and decode the token """
    decrypted = jwt.decode(encoded, PRIVATE_KEY, algorithms="HS256")
    email = decrypted["email"]

    query = await db.execute(select(models.User).where(models.User.email == email))
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(status_code=404, detail="Token expired.")
    
    return email 