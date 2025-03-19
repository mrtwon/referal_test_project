from fastapi import FastAPI

from src.app.middleware import add_application_exception_handler
from src.app.routes.v1.base import router
from src.app.dependency.base import di_all
import src.infrastructure.database.tables.user
import src.infrastructure.database.tables.user_referal

app = FastAPI()
app.include_router(router)
add_application_exception_handler(app)
di_all(app)
