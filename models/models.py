from sqlalchemy import MetaData, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from database.database import Base

metadata = MetaData()

#Декларативный метод записи
class Menu(Base):
    __tablename__ = "menus"

    id = Column(
                UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
                default=uuid4,
                )
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(
                UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
                default=uuid4,
                )
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id", ondelete='CASCADE'), nullable=False, )
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    dishes_count = Column(Integer, default=0)
    menu = relationship('Menu')


class Dishes(Base):
    __tablename__ = "dishes"

    id = Column(
                UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
                default=uuid4,
                )
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id", ondelete='CASCADE'), nullable=False, )
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    submenu = relationship('Submenu')
