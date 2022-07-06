from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete, select, insert

import datetime
import decimal 

from ssa import models, schemas 


async def get_calls (db: AsyncSession, skip: int = 0, limit: int = 100):
    query = await db.execute(select(models.Call).order_by(models.Call.id.desc()).limit(limit).offset(skip))
    return query.scalars().all()


async def get_call (db: AsyncSession, call_id: int, skip: int = 0, limit: int = 100):
    query = await db.execute(select(models.Call).where(models.Call.id == call_id))
    return query.scalars().first()


async def get_calls_by_author(db: AsyncSession, author_id: int, skip: int = 0, limit: int = 100):
    query = await db.execute(select(models.Call)
                    .where(models.Call.author_id == author_id)
                    .order_by(models.Call.id.desc())
                    .limit(limit)
                    .offset(skip))
    return query.scalars().all()


async def get_calls_by_author_email(db: AsyncSession, email: str, skip: int = 0, limit: int = 100):
    query = await db.execute(select(models.Call)
                    .join(models.User)
                    .where(models.User.email == email)
                    .order_by(models.Call.id.desc())
                    .limit(limit)
                    .offset(skip))
    return query.scalars().all()


async def get_calls_by_algorithm(db: AsyncSession, algorithm_id: int, skip: int = 0, limit: int = 100):
    query = await db.execute(select(models.Call)
                    .where(models.Call.algorithm_id == algorithm_id)
                    .order_by(models.Call.id.desc())
                    .limit(limit)
                    .offset(skip))
    return query.scalars().all()


async def get_calls_by_algorithm_name(db: AsyncSession, name: str, skip: int = 0, limit: int = 100):
    query = await db.execute(select(models.Call)
                    .join(models.Algorithm)
                    .where(models.Algorithm.name == name)
                    .order_by(models.Call.id.desc())
                    .limit(limit)
                    .offset(skip))
    return query.scalars().all()


async def create_call(db: AsyncSession, call: schemas.CallCreate, user_db: models.User, alg_db: models.Algorithm): 
    cost = decimal.Decimal(alg_db.cost)
    success = True if user_db.amount > cost else False 
    
    call_db = models.Call(
        datetime = datetime.datetime.now(),
        success = success,
        user_id = user_db.id,
        algorithm_id = call.algorithm_id
    )
    db.add(call_db)
    
    if success:
        await crud.create_transaction(db, user_db=alg_db.user, amount=decimal.Decimal(0.2) * cost)
        await crud.create_transaction(db, user_db=user_db, amount=-cost)

    await db.flush()
    return call_db

