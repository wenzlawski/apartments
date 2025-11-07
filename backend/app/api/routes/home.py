from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.utils import templates

router = APIRouter()

# Dummy datastore
items = ["Item 1", "Item 2"]

@router.get("/", response_class=HTMLResponse)
async def get_items(request: Request):
    return ""
