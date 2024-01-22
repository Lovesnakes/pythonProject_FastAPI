from typing import List, Dict

from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from database.database import get_db
from models.models import Submenu, Menu
from schemas.schemas import SubmenuSchemaOut, MenuSchemaBase

router = APIRouter()


@router.get("/")
async def get_submenu(db: Session = Depends(get_db)) -> List[SubmenuSchemaOut]:
    _submenu = db.query(Submenu).all()
    return _submenu


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_submenu(menus_id: UUID, submenu: MenuSchemaBase, db: Session = Depends(get_db)) -> SubmenuSchemaOut:
    _submenu = Submenu(**submenu.dict())
    _submenu.menu_id = menus_id
    db.add(_submenu)
    db.commit()
    db.refresh(_submenu)
    _menu = db.query(Menu).filter(Menu.id == _submenu.menu_id).first()
    _menu.submenus_count += 1
    db.commit()
    db.refresh(_menu)
    return _submenu


@router.get("/{submenu_id}")
async def get_submenu_id(submenu_id: UUID, db: Session = Depends(get_db)) -> SubmenuSchemaOut:
    _submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if not _submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return _submenu


@router.delete("/{submenu_id}")
def delete_submenu(submenu_id: UUID, db: Session = Depends(get_db)) -> Dict:
    _submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    db.delete(_submenu)
    db.commit()
    _menu = db.query(Menu).filter(Menu.id == _submenu.menu_id).first()
    _menu.submenus_count -= 1
    _menu.dishes_count -= _submenu.dishes_count
    db.commit()
    db.refresh(_menu)
    return {"status": True, "message": "The submenu has been deleted"}


@router.patch("/{submenu_id}")
def update_submenu(
        submenu_id: UUID, submenu: MenuSchemaBase, db: Session = Depends(get_db)) -> SubmenuSchemaOut:
    _submenu = db.query(Submenu).filter(Submenu.id == submenu_id)
    db_submenu = _submenu.first()
    if not _submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    _submenu.update(submenu.dict(exclude_unset=True))
    db.commit()
    db.refresh(db_submenu)
    return db_submenu
