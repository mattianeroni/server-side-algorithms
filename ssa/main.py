from typing import List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from ssa import crud, models, schemas
from ssa.database import engine, Base, async_session
from ssa.dependencies import get_session 
from ssa import api


app = FastAPI(title="ServerSideAlgorithms", docs_url="/docs", redoc_url="/redocs")

app.mount("/static", StaticFiles(directory="static"), name="static")

# To restart the database
#@app.on_event("startup")
#async def startup():
#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.drop_all)
#        await conn.run_sync(Base.metadata.create_all)

#@app.middleware("http")
#async def mid(request: Request, call_next):
#    print("Middleware")
#    return await call_next(request)

app.include_router(api.users.router)
app.include_router(api.categories.router)
app.include_router(api.algorithms.router)
app.include_router(api.calls.router)
app.include_router(api.auth.router)
app.include_router(api.website.router)




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

