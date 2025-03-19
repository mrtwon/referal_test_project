from fastapi import FastAPI, Depends

from src.domain.base.interface import IUoW
from src.domain.user.service.user import UserServiceABC
from src.implementation.user.service.user import UserService


def get_user_service(
        uow: IUoW = Depends()
):
    return UserService(uow, uow)


def di_user(app: FastAPI):
    app.dependency_overrides[UserServiceABC] = get_user_service
