from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["home"])

# Dummy datastore
items = ["Item 1", "Item 2"]


@router.get("/", response_class=HTMLResponse)
async def get_items(request: Request):
    return ""
