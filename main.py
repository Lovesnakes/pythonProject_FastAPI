from fastapi import FastAPI
import uvicorn
from endpoints import menu, submenu, dish


app = FastAPI(title="Меню ресторана")


app.include_router(menu.router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(submenu.router, prefix="/api/v1/menus/{menus_id}/submenus", tags=["submenus"])
app.include_router(dish.router, prefix="/api/v1/menus/{menus_id}/submenus/{submenu_id}/dishes", tags=["dishes"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
