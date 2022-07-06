from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_token


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"},
        409 : {"description": "Conflict"},
        422 : {"description": "Unprocessable entity"}
    }
)



@router.get("/", response_model=List[schemas.Transaction])
async def get_transactions(token: str, db: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100):
    user_db = await verify_token(db, token)
    return await crud.get_transactions(db, user_id=user_db.id, skip=skip, limit=limit)
    