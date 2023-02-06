from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ssa import models, schemas, crud
from ssa.dependencies import get_session, verify_token, verify_token_admin


router = APIRouter(
    prefix="/algorithms",
    tags=["algorithms"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"},
        409 : {"description": "Conflict"},
        422 : {"description": "Unprocessable entity"}
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

    user_db = await verify_token_admin(db, token=algorithm.token)
    
    return await crud.create_algorithm(db, algorithm=algorithm)


@router.delete("/")
async def delete_algorithm(algorithm: schemas.AlgorithmDelete, db: AsyncSession = Depends(get_session)):
    algorithm_db = await crud.get_algorithm(db, alg_id=algorithm.id)
    if not algorithm_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    user_db = await verify_token_admin(db, token=algorithm.token)

    res = await crud.delete_algorithm(db, alg_id=algorithm.id)
    return {"ok" : res}


@router.put("/", response_model=schemas.Algorithm)
async def update_algorithm(algorithm: schemas.AlgorithmUpdate, db: AsyncSession = Depends(get_session)):
    alg_db = await crud.get_algorithm(db, alg_id=algorithm.id)
    if not alg_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    alg_db_samename = await crud.get_algorithm_by_name(db, name=algorithm.name)
    if alg_db_samename and alg_db_samename != alg_db:
        raise HTTPException(status_code=400, detail="Algorithm name already existing.")
    
    user_db = await verify_token_admin(db, token=algorithm.token)
    
    return await crud.update_algorithm(db, algorithm, alg_db)


@router.put("/", response_model=schemas.Algorithm)
async def validate_algorithm(algorithm : schemas.AlgorithmValidate, db: AsyncSession = Depends(get_session)):
    alg_db = await crud.get_algorithm(db, alg_id=algorithm.id)
    if not alg_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    admin_db = await verify_token_admin(db, token=algorithm.token)

    await crud.validate_algorithm(db, alg_id=algorithm.id)
    return alg_db



@router.post("/upload/readme", response_model=schemas.Algorithm)
async def upload_readme(id: int = Form(...), token: str = Form(...), file: UploadFile = File(default=None), db: AsyncSession = Depends(get_session)):
    if not file:
        raise HTTPException(status_code=400, detail="File object not provided.")

    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Wrong file format. It should be text/plain.")

    user_db = await verify_token_admin(db, token)

    alg_db = await crud.get_algorithm(db, alg_id=id)
    if not alg_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    if alg_db.author_id != user_db.id:
        raise HTTPException(status_code=409, detail="Only the author can update an algorithm.")
    
    return await crud.upload_readme(db, file=file, alg_db=alg_db)


@router.post("/upload/code", response_model=schemas.Algorithm)
async def upload_code(id: int = Form(...), token: str = Form(...), file: UploadFile = File(default=None), db: AsyncSession = Depends(get_session)):
    if not file:
        raise HTTPException(status_code=400, detail="File object not provided.")

    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Wrong file format. It should be text/plain.")

    user_db = await verify_token_admin(db, token)

    alg_db = await crud.get_algorithm(db, alg_id=id)
    if not alg_db:
        raise HTTPException(status_code=404, detail="Algorithm not found.")

    if alg_db.author_id != user_db.id:
        raise HTTPException(status_code=409, detail="Only the author can update an algorithm.")
    
    return await crud.upload_code(db, file=file, alg_db=alg_db)
    