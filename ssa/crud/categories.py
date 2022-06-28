from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete, select, insert

from ssa import models, schemas 



async def get_category(db : AsyncSession, cat_id : int):
    """ GET method to get a category from its id. """
    query = await db.execute(
        select(models.Category)
            .where(models.Category.id == cat_id)
            .options(selectinload(models.Category.algorithms))
    )
    return query.scalars().first()


async def get_category_by_name(db : AsyncSession, name : str):
    """ GET method to get a category from its name """
    query = await db.execute(select(models.Category).where(models.Category.name == name))
    return query.scalars().first()


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """ GET method to get all categories at once """
    query = await db.execute(select(models.Category).order_by(models.Category.id).limit(limit).offset(skip))
    return query.scalars().all()


async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    """ POST method to create category """
    db_category = models.Category(**category.dict())
    db.add(db_category)
    await db.flush()
    return db_category


async def delete_category(db: AsyncSession, cat_id: int):
    """ DELETE method to delete a category """
    await db.execute(delete(models.Category).where(models.Category.id == cat_id))
    return True

async def update_category(db: AsyncSession, category: schemas.CategoryUpdate, cat_db: models.Category):
    """ PUT method to update a category """
    name, desc = category.name or cat_db.name, category.desc or cat_db.desc
    await db.execute(update(models.Category).where(models.Category.id == category.id).values(name=name, desc=desc))
    return cat_db