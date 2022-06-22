from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ssa import models, schemas, crud
from ssa.dependencies import get_session, get_templates, verify_user_by_email, verify_user


router = APIRouter(
    tags=["auth"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"},
        409 : {"description": "Conflict"},
    },
    include_in_schema=False,
)



@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    #form = await request.json()
    #print( form )
    return templates.TemplateResponse("/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    
    return templates.TemplateResponse("/index.html", {"request": request})