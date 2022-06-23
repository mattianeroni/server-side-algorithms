from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_user_by_email, create_token


router = APIRouter(
    prefix="/",
    tags=["auth"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"}
    }
)


@router.post("/login")
def login (user: schemas.Login, db: AsyncSession = Depends(get_session)):
    res = await verify_user_by_email(db, email=user.email, password=user.password)
    if not res:
        raise HTTPException(status_code=400, detail="Uncorrect user details.")
    token = await create_token(user.email)
    return {"token" : token}
