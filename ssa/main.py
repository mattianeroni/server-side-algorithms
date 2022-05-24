from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ssa import crud, models, schemas
from ssa.database import engine, Base, async_session
from ssa.dependencies import get_session 


app = FastAPI(title="ServerSideAlgorithms")


#@app.on_event("startup")
#async def startup():
#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.drop_all)
#        await conn.run_sync(Base.metadata.create_all)



# Users end points from here.

@app.post("/users/", response_model=schemas.UserWithKey)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.UserBasic])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user


@app.delete("/users/")
async def delete_user(user: schemas.UserDelete, db: AsyncSession = Depends(get_session)):
    res = await crud.delete_user(db, user)
    if not res:
        raise HTTPException(status_code=404, detail="Password not correct or user not registered.")
    return {"response" : res}




# Categories end points from here.

@app.post("/categories/", response_model=schemas.CategoryBasic)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_session)):
    db_cat = await crud.get_category_by_name(db, name=category.name)
    if db_cat:
        raise HTTPException(status_code=400, detail="Category name already existing.")
    return await crud.create_category(db, category=category)


@app.get("/categories/", response_model=List[schemas.CategoryBasic])
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await crud.get_categories(db, skip=skip, limit=limit)


@app.get("/categories/{cat_id}", response_model=schemas.Category)
async def get_category(cat_id: int, db: AsyncSession = Depends(get_session)):
    db_cat = await crud.get_category(db, cat_id=cat_id)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    return db_cat




#from fastapi import File, UploadFile
#import aiofiles

#@app.post("/upload")
#async def upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
#    try:
#        contents = await file.read()
#        async with aiofiles.open(file.filename, 'wb') as f:
#            await f.write(contents)
#    except Exception:
#        return {"message": "There was an error uploading the file"}
#    finally:
#        await file.close()
#
#    return {"message": f"Successfuly uploaded {file.filename}"}

