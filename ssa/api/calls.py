from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_key_by_email


router = APIRouter(
    prefix="/calls",
    tags=["calls"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"}
    }
)


@router.get("/", response_model=List[schemas.Call])
async def get_calls(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await crud.get_calls(db, skip=skip, limit=limit)


@router.get("/{call_id}", response_model=schemas.Call)
async def get_call(call_id : int, db: AsyncSession = Depends(get_session)):
    db_call = await crud.get_call(db, call_id=call_id)
    if not db_call:
        raise HTTPException(status_code=404, detail="Call not found.")
    return db_call


@router.post("/", response_model=schemas.Call)
async def create_call(call_create: schemas.CallCreate, db: AsyncSession = Depends(get_session)):
    res = await verify_key_by_email(db, email=call_create.email, personal_key=call_create.personal_key)
    if not res:
        raise HTTPException(status_code=400, detail="Uncorrect user details.")

    alg_db = await crud.get_algorithm(db, alg_id=call_create.algorithm_id)
    if not alg_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")
    
    return await crud.create_call(db, call_create)