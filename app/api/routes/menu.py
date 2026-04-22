from __future__ import annotations

from fastapi import APIRouter
from app.api.services.menu import get_menu

router = APIRouter()

@router.get("/getmenu")
def getmenu_endpoint() -> dict:
    menu_list = get_menu()
    formatted_menu = [{"name": name, "price": price} for name, price in menu_list]
    return {
        "status": "success",
        "data": formatted_menu
    }
