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

async def verify_user(db: AsyncSession, user_id: int, password: str):
    query = await db.execute(select(models.User).where(models.User.id == user_id))
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_db.password != crypt.crypt(password, salt=user_db.salt):
        return False
    
    return True


async def verify_key(db: AsyncSession, user_id: int, personal_key: str):
    query = await db.execute(select(models.User).where(models.User.id == user_id))
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_db.personal_key != crypt.crypt(personal_key, salt=user_db.salt_key):
        return False
    
    return True


async def verify_user_by_email(db: AsyncSession, email: EmailStr, password: str):
    query = await db.execute(select(models.User).where(models.User.email == email))
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_db.password != crypt.crypt(password, salt=user_db.salt):
        return False
    
    return True


async def verify_key_by_email(db: AsyncSession, email: EmailStr, personal_key: str):
    query = await db.execute(select(models.User).where(models.User.email == email))
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_db.personal_key != crypt.crypt(personal_key, salt=user_db.salt_key):
        return False
    
    return True