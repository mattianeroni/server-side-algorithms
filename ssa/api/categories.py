from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ssa import models, schemas, crud
from ssa.dependencies import get_session


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"},
        409 : {"description": "Conflict"}
    }
)



@router.post("/", response_model=schemas.CategoryBasic)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_session)):
    db_cat = await crud.get_category_by_name(db, name=category.name)
    if db_cat:
        raise HTTPException(status_code=400, detail="Category name already existing.")
    return await crud.create_category(db, category=category)



@router.get("/", response_model=List[schemas.CategoryBasic])
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await crud.get_categories(db, skip=skip, limit=limit)



@router.get("/{cat_id}", response_model=schemas.Category)
async def get_category(cat_id: int, db: AsyncSession = Depends(get_session)):
    db_cat = await crud.get_category(db, cat_id=cat_id)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    return db_cat



@router.get("/{cat_id}/algorithms", response_model=List[schemas.AlgorithmBasic])
async def get_algorithms_by_category(cat_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await crud.get_algorithms_by_category(db, cat_id=cat_id, skip=skip, limit=limit)



@router.delete("/{cat_id}")
async def delete_category(cat_id: int, db: AsyncSession = Depends(get_session)):
    algorithms = await crud.get_algorithms_by_category(db, cat_id)
    if algorithms:
        raise HTTPException(status_code=409, detail="Cannot delete category with algorithms.")
    
    res = await crud.delete_category(db, cat_id)
    if not res:
        raise HTTPException(status_code=400, detail="Category not found.")
    return {"ok" : res}