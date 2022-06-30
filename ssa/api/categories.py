from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_token_admin, verify_token


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
    user_db = await verify_token(db, token=category.token)
    cat_db = await crud.get_category_by_name(db, name=category.name)
    if cat_db:
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


@router.delete("/")
async def delete_category(category: schemas.CategoryDelete, db: AsyncSession = Depends(get_session)):
    user_db = await verify_token_admin(db, token=category.token)

    algorithms = await crud.get_algorithms_by_category(db, cat_id=category.id)
    if algorithms:
        raise HTTPException(status_code=409, detail="Cannot delete category with algorithms.")
    
    res = await crud.delete_category(db, cat_id=category.id)
    if not res:
        raise HTTPException(status_code=400, detail="Category not found.")
    return {"ok" : res}


@router.put("/", response_model=schemas.Category)
async def update_category(category: schemas.CategoryUpdate, db: AsyncSession = Depends(get_session)):
    user_db = await verify_token_admin(db, token=category.token)

    cat_db = await crud.get_category(db, cat_id=category.id)
    if not cat_db:
        raise HTTPException(status_code=404, detail="Category not found.")

    cat_db_samename = await crud.get_category_by_name(db, name=category.name)
    if cat_db_samename and cat_db_samename != cat_db:
        raise HTTPException(status_code=400, detail="Category name already existing.")
    
    return await crud.update_category(db, category, cat_db)