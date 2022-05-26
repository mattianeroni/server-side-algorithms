from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_key


router = APIRouter(
    prefix="/algorithms",
    tags=["algorithms"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"}
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
    # Check the algorithm is not registered
    algorithm_db = await crud.get_algorithm_by_name(db, algorithm.name)
    if algorithm_db:
        raise HTTPException(status_code=400, detail="Name already registered.")

    # Check category exists
    category_db = await crud.get_category_by_name(db, name=algorithm.category_name)
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found.")

    # Check authentication
    res = await verify_key(db, email=algorithm.author_email, personal_key=algorithm.personal_key)
    if not res:
        raise HTTPException(status_code=400, detail="Uncorrect user details.")
    
    return await crud.create_algorithm(db, algorithm)


    
    

    