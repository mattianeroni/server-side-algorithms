from typing import List
from fastapi import FastAPI, HTTPException, Depends, Request
#from fastapi.staticfiles import StaticFiles
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from ssa import crud, models, schemas
from ssa.database import engine, Base, async_session
from ssa.dependencies import get_session 
from ssa import api

import os 


app = FastAPI(title="ServerSideAlgorithms", docs_url="/docs", redoc_url="/redocs", openapi_url=None)

#app.mount("/static", StaticFiles(directory="static"), name="static")

# To restart the database
#@app.on_event("startup")
#async def startup():
#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.drop_all)
#        await conn.run_sync(Base.metadata.create_all)
#    for i in os.listdir("./documentation/code/") + os.listdir("./documentation/readme/"):
#        os.remove(i)


#app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(api.users.router)
app.include_router(api.categories.router)
app.include_router(api.algorithms.router)
app.include_router(api.calls.router)
app.include_router(api.auth.router)
app.include_router(api.transactions.router)
#app.include_router(api.website.router)


#import uvicorn

#if __name__ == '__main__':
#    uvicorn.run("app.main:app",
#                host="127.0.0.1",
#                port=8000,
#                reload=True,
#                ssl_keyfile="./key.pem", 
#                ssl_certfile="./cert.pem"
#                )
