from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_token


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
    call_db = await crud.get_call(db, call_id=call_id)
    if not call_db:
        raise HTTPException(status_code=404, detail="Call not found.")
    return call_db


@router.post("/", response_model=schemas.Call)
async def create_call(call_create: schemas.CallCreate, db: AsyncSession = Depends(get_session)):
    user_db = await verify_token(db, token=call_create.token)
    
    alg_db = await crud.get_algorithm(db, alg_id=call_create.algorithm_id)
    if not alg_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    if user_db.amount > alg_db.cost:
        create_call.success = True
    else:
        create_call.success = False
    
    return await crud.create_call(db, call_create=call_create, user_id=user_db.id)