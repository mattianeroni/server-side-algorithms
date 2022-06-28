from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi.templating import Jinja2Templates

from ssa import models, schemas, crud
from ssa.dependencies import get_session, get_templates

router = APIRouter(
    tags=["website"],
    responses = {
        404 : {"description": "Not found"}, 
        400 : {"description": "Bad request"},
        409 : {"description": "Conflict"},
    },
    include_in_schema=False,
)



@router.get("/", response_class=HTMLResponse)
async def home(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("/index.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("/about.html", {"request": request})