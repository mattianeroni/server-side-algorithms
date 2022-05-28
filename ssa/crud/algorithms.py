from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete, select, insert, join
from pydantic import EmailStr 

from ssa import models, schemas 

from sqlalchemy.exc import SQLAlchemyError



async def get_algorithms(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = await db.execute(select(models.Algorithm).order_by(models.Algorithm.id).limit(limit).offset(skip))
    return query.scalars().all()



async def get_algorithms_by_category(db: AsyncSession, cat_id: int, skip: int = 0, limit: int = 100):
    query = await db.execute(
        select(models.Algorithm).where(models.Algorithm.category_id == cat_id)
        .order_by(models.Algorithm.id)
        .limit(limit)
        .offset(skip)
    )
    return query.scalars().all()



async def get_algorithms_by_author(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    query = await db.execute(
        select(models.Algorithm).where(models.Algorithm.author_id == user_id)
        .order_by(models.Algorithm.id)
        .limit(limit)
        .offset(skip)
    )
    return query.scalars().all()


async def get_algorithms_by_author_email(db: AsyncSession, email: EmailStr, skip: int = 0, limit: int = 100):
    query = await db.execute(
        select(models.Algorithm).join(models.User).where(models.User.email == email)
        .order_by(models.Algorithm.id)
        .limit(limit)
        .offset(skip)
    )
    return query.scalars().all()



async def get_algorithm(db: AsyncSession, alg_id: int):
    query = await db.execute(
        select(models.Algorithm)
            .where(models.Algorithm.id == alg_id)
            .options(selectinload(models.Algorithm.calls))
            .options(selectinload(models.Algorithm.category))
    )
    return query.scalars().first()



async def get_algorithm_by_name(db: AsyncSession, name: str):
    query = await db.execute(select(models.Algorithm).where(models.Algorithm.name == name))
    return query.scalars().first()



async def create_algorithm(db: AsyncSession, algorithm: schemas.AlgorithmCreate):
    algorithm_db = models.Algorithm(
        name = algorithm.name,
        author_id = algorithm.author_id,
        category_id = algorithm.category_id,
        desc = algorithm.desc,
        cost = algorithm.cost,
        readme = algorithm.readme
    )
    db.add(algorithm_db)
    await db.flush()
    return algorithm_db
    
    