from typing import List, Dict

from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from database.database import get_db
from models.models import Menu
from schemas.schemas import MenuSchemaOut, MenuSchemaBase

router = APIRouter()


# Просмотр списка меню
@router.get("/")
async def get_menu(db: Session = Depends(get_db)) -> List[MenuSchemaOut]:
    _menu = db.query(Menu).all()
    return _menu


# Добавление нового меню
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_menu(menu: MenuSchemaBase, db: Session = Depends(get_db)
                 ) -> MenuSchemaOut:
    _menu = Menu(**menu.dict())
    db.add(_menu)
    db.commit()
    db.refresh(_menu)
    return _menu


#Просмотр определенного меню
@router.get("/{menu_id}")
async def get_menu_id(menu_id: UUID, db: Session = Depends(get_db)) -> MenuSchemaOut:
    _menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not _menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return _menu


# Удвление меню
@router.delete("/{menu_id}")
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)
                 ) -> Dict:
    _menu = db.query(Menu).filter(Menu.id == menu_id).first()
    db.delete(_menu)
    db.commit()
    return {"status": True, "message": "The menu has been deleted"}


# Редактирование меню
@router.patch("/{menu_id}")
def update_menu(
        menu_id: UUID, submenu: MenuSchemaBase, db: Session = Depends(get_db)
) -> MenuSchemaOut:
    _menu = db.query(Menu).filter(Menu.id == menu_id)
    db_menu = _menu.first()
    try:
        _menu.update(submenu.dict(exclude_unset=True))
        db.commit()
        db.refresh(db_menu)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return db_menu
