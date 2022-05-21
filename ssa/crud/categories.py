from sqlalchemy.orm import Session
from ssa import models, schemas 



async def get_category(db : Session, cat_id : int):
    return await db.query(models.Category).filter(models.Category.id == cat_id).first()


async def get_category_by_name(db : Session, name : str):
    return async db.query(models.Category).filter(models.Category.name == name).first()


async def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(models.Category).offset(skip).limit(limit).all()


async def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    await db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(db: Session, cat_id: int):
    await db.query(models.Category).filter(models.Category.id == cat_id).delete()
    await db.commit()


async def delete_category_by_name(db: Session, name: str):
    await db.query(models.Category).filter(models.Category.name == name).delete()
    await db.commit()


async def update_category(db: Session, category: schemas.CategoryUpdate, cat_id: int):
    await db.query(models.Category).filter(models.Category.id == cat_id).update(**category.dict())
    await db.commit()