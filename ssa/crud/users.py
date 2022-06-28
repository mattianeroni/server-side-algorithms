from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete, select, insert


from ssa import models, schemas 

import crypt
import asyncio
import decimal
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
    query = await db.execute(
        select(models.User)
            .where(models.User.email == email)
            .options(selectinload(models.User.calls))
            .options(selectinload(models.User.algorithms))
    )
    return query.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """ GET method to get all users at once """
    query = await db.execute(select(models.User).order_by(models.User.id).limit(limit).offset(skip))
    return query.scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """ POST method to create a new user """
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    password = crypt.crypt(user.password, salt=salt)

    db_user = models.User(
        email=user.email, 
        password=password, 
        salt=salt, 
        amount=user.amount
    )
    db.add(db_user)
    await db.flush()
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    """ DELETE method to delete a user """
    await db.execute(delete(models.User).where(models.User.id == user_id))
    return True


async def update_user(db: AsyncSession, user: schemas.UserUpdate, user_db: models.User):
    """ PUT method to update a user email and password """
    email = user.email
    password, salt = user_db.password, user_db.salt 
    if user.password is not None:
        salt = crypt.mksalt(crypt.METHOD_SHA512)
        password = crypt.crypt(user.password, salt=salt)

    await db.execute(update(models.User).where(models.User.id == user_db.id).values(email=email, password=password, salt=salt))
    return user_db


async def update_user_amount(db: AsyncSession, amount: float, user_db: models.User):
    """ PUT method to update a user amount """
    user_db.amount += decimal.Decimal(amount)
    await db.flush()
    return user_db

    
