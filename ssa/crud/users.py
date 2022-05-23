from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from sqlalchemy.future import select

from ssa import models, schemas 

import crypt
import hmac
import string 
import secrets 



async def get_user(db: AsyncSession, user_id: int):
    """ GET method to get a user from his/her id. """
    try:
        query = await db.execute(
            select(models.User)
                .where(models.User.id == user_id)
                .options(selectinload(models.User.calls))
                .options(selectinload(models.User.algorithms))
        )
        return query.scalars().first()
    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))



async def get_user_by_email(db: AsyncSession, email: str):
    """ GET method to get a user from his/her email. """
    try:
        query = await db.execute(select(models.User).where(models.User.email == email))
        return query.scalars().first()
    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))



async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """ GET method to get all users at once """
    try:
        query = await db.execute(select(models.User).order_by(models.User.id).limit(limit).offset(skip))
        return query.scalars().all()
    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))



async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """ POST method to create a new user """
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    password = crypt.crypt(user.password, salt=salt)

    key = "".join([secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16)])
    salt_key = crypt.mksalt(crypt.METHOD_SHA512)
    personal_key = crypt.crypt(key, salt=salt_key)

    try:
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

        db_user.personal_key = key
        return db_user

    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))



async def delete_user(db: AsyncSession, user: schemas.UserDelete):
    """ DELETE method to delete a user """
    try:
        query = await db.execute(select(models.User).where(models.User.email == user.email))
        db_user = query.scalars().first()

        if db_user.password != crypt.crypt(user.password, salt=db_user.salt):
            return False
    
        await db.delete(db_user)
        await db.commit()
        return True

    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))




#async def update_user(db: Session, new_user: schemas.UserUpdate, user_id: int):
#    await db.query(models.User).filter(models.User.id == user_id).update(**new_user.dict())
#    await db.commit()


#async def update_user_amount(db: Session, user_id: int, amount: float):
#    user = await db.query(models.User).filter(models.User.id == user_id).first()
#    user.amount += amount
#    await db.commit()
#    await db.refresh(user)
