from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_token


router = APIRouter(
    prefix="/algorithms",
    tags=["algorithms"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"},
        409 : {"description": "Conflict"}
    }
)



@router.get("/", response_model=List[schemas.AlgorithmBasic])
async def get_algorithms(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await crud.get_algorithms(db, skip=skip, limit=limit)


@router.get("/{alg_id}", response_model=schemas.Algorithm)
async def get_algorithm(alg_id: int, db: AsyncSession = Depends(get_session)):
    algorithm_db = await crud.get_algorithm(db, alg_id=alg_id)
    if not algorithm_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")
    return algorithm_db


@router.post("/", response_model=schemas.AlgorithmBasic)
async def create_algorithm(algorithm: schemas.AlgorithmCreate, db: AsyncSession = Depends(get_session)):
    algorithm_db = await crud.get_algorithm_by_name(db, name=algorithm.name)
    if algorithm_db:
        raise HTTPException(status_code=400, detail="Name already registered.")

    category_db = await crud.get_category(db, cat_id=algorithm.category_id)
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found.")

    user_db = await verify_token(db, token=algorithm.token)
    
    return await crud.create_algorithm(db, algorithm=algorithm, user_id=user_db.id)


@router.delete("/")
async def delete_algorithm(algorithm: schemas.AlgorithmDelete, db: AsyncSession = Depends(get_session)):
    algorithm_db = await crud.get_algorithm(db, alg_id=algorithm.id)
    if not algorithm_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    user_db = await verify_token(db, token=algorithm.token)
    if user_db.id != algorithm_db.author_id:
        raise HTTPException(status_code=409, detail="Only the author can delete an algorithm.")

    res = await crud.delete_algorithm(db, alg_id=algorithm.id)
    return {"ok" : res}


@router.put("/", response_model=schemas.Algorithm)
async def update_algorithm(algorithm: schemas.AlgorithmUpdate, db: AsyncSession = Depends(get_session)):
    alg_db = await crud.get_algorithm(db, alg_id=algorithm.id)
    if not alg_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    alg_db_samename = await crud.get_algorithm_by_name(db, name=algorithm.name)
    if alg_db_samename:
        raise HTTPException(status_code=400, detail="Algorithm name already existing.")
    
    user_db = await verify_token(db, token=algorithm.token)
    if user_db.id != algorithm_db.author_id:
        raise HTTPException(status_code=409, detail="Only the author can update an algorithm.")
    
    return await crud.update_algorithm(db, algorithm, alg_db)

    