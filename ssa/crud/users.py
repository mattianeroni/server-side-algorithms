from sqlalchemy.orm import Session, selectinload
from sqlalchemy import update
from sqlalchemy.future import select

from ssa import models, schemas 

import crypt
import hmac
import string 
import secrets 



async def get_user(db: Session, user_id: int):
    query = await db.execute(
        select(models.User)
            .where(models.User.id == user_id)
            .options(selectinload(models.User.calls))
            .options(selectinload(models.User.algorithms))
    )
    return query.scalars().first()


async def get_user_by_email(db: Session, email: str):
    query = await db.execute(select(models.User).where(models.User.email == email))
    return query.scalars().first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):    
    query = await db.execute(select(models.User).order_by(models.User.id).limit(limit).offset(skip))
    return query.scalars().all()


async def create_user(db: Session, user: schemas.UserCreate):
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

    db_user.personal_key = key
    return db_user


#async def delete_user(db: Session, user_id: int):
#    await db.query(models.User).filter(models.User.id == user_id).delete()
#    await db.commit()


#async def delete_user_by_email(db: Session, email: str):
#    await db.query(models.User).filter(models.User.email == email).delete()
#    await db.commit()


#async def update_user(db: Session, new_user: schemas.UserUpdate, user_id: int):
#    await db.query(models.User).filter(models.User.id == user_id).update(**new_user.dict())
#    await db.commit()


#async def update_user_amount(db: Session, user_id: int, amount: float):
#    user = await db.query(models.User).filter(models.User.id == user_id).first()
#    user.amount += amount
#    await db.commit()
#    await db.refresh(user)
