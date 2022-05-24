from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from sqlalchemy.future import select

from ssa import models, schemas 



async def get_category(db : AsyncSession, cat_id : int):
    """ GET method to get a category from its id. """
    try:
        query = await db.execute(
            select(models.Category)
                .where(models.Category.id == cat_id)
                .options(selectinload(models.Category.algorithms))
        )
        return query.scalars().first()
    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))



async def get_category_by_name(db : AsyncSession, name : str):
    """ GET method to get a category from its name """
    try:
        query = await db.execute(select(models.Category).where(models.Category.name == name))
        return query.scalars().first()
    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))



async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """ GET method to get all categories at once """
    try:
        query = await db.execute(select(models.Category).order_by(models.Category.id).limit(limit).offset(skip))
        return query.scalars().all()
    except SQLAlchemyError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(exception))



async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    """ POST method to create category """
    db_category = models.Category(**category.dict())
    db.add(db_category)
    await db.flush()
    return db_category


#async def delete_category(db: AsyncSession, cat_id: int):
#    await db.query(models.Category).filter(models.Category.id == cat_id).delete()
#    await db.commit()


#async def delete_category_by_name(db: AsyncSession, name: str):
#    await db.query(models.Category).filter(models.Category.name == name).delete()
#    await db.commit()


#async def update_category(db: AsyncSession, category: schemas.CategoryUpdate, cat_id: int):
#    await db.query(models.Category).filter(models.Category.id == cat_id).update(**category.dict())
#    await db.commit()