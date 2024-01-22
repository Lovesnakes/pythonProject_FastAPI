from typing import List, Dict

from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from database.database import get_db
from models.models import Dishes, Submenu, Menu
from schemas.schemas import DishSchemaOut, DishSchemaBase

router = APIRouter()


# Просмотр списка блюд
@router.get("/")
async def get_dishes(db: Session = Depends(get_db)) -> List[DishSchemaOut]:
    _dish = db.query(Dishes).all()
    return _dish


# Создание блюда
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_dishes(submenu_id: UUID, dish: DishSchemaBase, db: Session = Depends(get_db)
                  ) -> DishSchemaOut:
    _dish = Dishes(**dish.dict())
    dish_price = round(float(_dish.price), 2)
    _dish.price = str(dish_price)
    _dish.submenu_id = submenu_id
    db.add(_dish)
    db.commit()
    db.refresh(_dish)
    _submenu = db.query(Submenu).filter(Submenu.id == _dish.submenu_id).first()
    _submenu.dishes_count += 1
    db.commit()
    db.refresh(_submenu)
    _menu = db.query(Menu).filter(Menu.id == _submenu.menu_id).first()
    _menu.dishes_count += 1
    db.commit()
    db.refresh(_menu)
    return _dish


# Просмотр блюда
@router.get("/{dish_id}")
async def get_dish_id(dish_id: UUID, db: Session = Depends(get_db)) -> DishSchemaOut:
    _dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    if not _dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return _dish


# Удаление блюда
@router.delete("/{dish_id}")
def delete_menus(dish_id: UUID, db: Session = Depends(get_db)
                 ) -> Dict:
    _dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    db.delete(_dish)
    db.commit()
    _submenu = db.query(Submenu).filter(Submenu.id == _dish.submenu_id).first()
    _submenu.dishes_count -= 1
    db.commit()
    db.refresh(_submenu)
    _menu = db.query(Menu).filter(Menu.id == _submenu.menu_id).first()
    _menu.dishes_count -= 1
    db.commit()
    db.refresh(_menu)
    return {"status": True, "message": "The dish has been deleted"}


# Редактирование блюда
@router.patch("/{dish_id}")
def update(
        dish_id: UUID, dish: DishSchemaBase, db: Session = Depends(get_db)
) -> DishSchemaOut:
    _dish = db.query(Dishes).filter(Dishes.id == dish_id)
    db_dish = _dish.first()
    dish.price = str(round(float(dish.price), 2))
    try:
        _dish.update(dish.dict(exclude_unset=True))
        db.commit()
        db.refresh(db_dish)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    return db_dish
