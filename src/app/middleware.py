from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from src.domain.base.exception import AppBaseException


def add_application_exception_handler(app: FastAPI):
    @app.exception_handler(AppBaseException)
    async def handler(request: Request, exc: AppBaseException):
        raise HTTPException(detail=exc.detail, status_code=exc.status)
