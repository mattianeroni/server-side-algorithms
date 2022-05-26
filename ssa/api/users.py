from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ssa import models, schemas, crud
from ssa.dependencies import get_session


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"}
    }
)

@router.post("/", response_model=schemas.UserWithKey)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return await crud.create_user(db, user=user)


@router.get("/", response_model=List[schemas.UserBasic])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user


@router.delete("/")
async def delete_user(user: schemas.UserDelete, db: AsyncSession = Depends(get_session)):
    res = await crud.delete_user(db, user)
    if not res:
        raise HTTPException(status_code=404, detail="Password not correct or user not registered.")
    return {"ok" : res}