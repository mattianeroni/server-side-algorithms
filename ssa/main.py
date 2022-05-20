from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List

from ssa import crud, models, schemas
from ssa.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ServerSideAlgorithms")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Users end points from here.

@app.post("/users/", response_model=schemas.UserWithKey)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.UserBasic])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user



# Categories end points from here.

@app.post("/categories/", response_model=schemas.CategoryBasic)
def create_user(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_cat = crud.get_category_by_name(db, name=category.name)
    if db_cat:
        raise HTTPException(status_code=400, detail="Category name already existing.")
    return crud.create_category(db, category=category)


@app.get("/categories/", response_model=List[schemas.CategoryBasic])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/categories/{cat_id}", response_model=schemas.Category)
def get_category(cat_id: int, db: Session = Depends(get_db)):
    db_cat = crud.get_category(db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Category not found.")
    return db_cat




#from fastapi import File, UploadFile
#import aiofiles

#@app.post("/upload")
#async def upload(file: UploadFile = File(...)):
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

