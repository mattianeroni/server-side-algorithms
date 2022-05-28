from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete, select, insert


from ssa import models, schemas 

import crypt
import hmac
import string 
import secrets 


import asyncio
import pandas as pd
from ssa.database import engine 


async def get_user(db: AsyncSession, user_id: int):
    """ GET method to get a user from his/her id. """
    query = await db.execute(
        select(models.User)
            .where(models.User.id == user_id)
            .options(selectinload(models.User.calls))
            .options(selectinload(models.User.algorithms))
    )
    return query.scalars().first()



async def get_user_by_email(db: AsyncSession, email: str):
    """ GET method to get a user from his/her email. """
    query = await db.execute(select(models.User).where(models.User.email == email))
    return query.scalars().first()



async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """ GET method to get all users at once """
    query = await db.execute(select(models.User).order_by(models.User.id).limit(limit).offset(skip))
    return query.scalars().all()



async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """ POST method to create a new user """
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    password = crypt.crypt(user.password, salt=salt)

    key = "".join([secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16)])
    salt_key = crypt.mksalt(crypt.METHOD_SHA512)
    personal_key = crypt.crypt(key, salt=salt_key)

    db_user = models.User(
        email=user.email, 
        password=password, 
        salt=salt, 
        salt_key=salt_key,
        personal_key=personal_key,
        amount=user.amount
    )
    db.add(db_user)
    await db.flush()
    return schemas.UserWithKey(id=db_user.id, email=user.email, personal_key=key)



async def delete_user(db: AsyncSession, user: schemas.UserDelete):
    """ DELETE method to delete a user """
    await db.execute(delete(models.User).where(models.User.email == user.email))
    return True




#async def update_user(db: Session, new_user: schemas.UserUpdate, user_id: int):
#    await db.query(models.User).filter(models.User.id == user_id).update(**new_user.dict())
#    await db.commit()


#async def update_user_amount(db: Session, user_id: int, amount: float):
#    user = await db.query(models.User).filter(models.User.id == user_id).first()
#    user.amount += amount
#    await db.commit()
#    await db.refresh(user)
