from fastapi import FastAPI, Depends

from src.domain.base.interface import IUoW
from src.domain.user.service.user import UserServiceABC
from src.domain.user_referal.service.user_referal import UserReferalServiceABC
from src.implementation.user.service.user import UserService
from src.implementation.user_referal.service.user_referal import UserReferalService


def get_user_service(
        uow: IUoW = Depends()
):
    return UserReferalService(uow)


def di_user_referal(app: FastAPI):
    app.dependency_overrides[UserReferalServiceABC] = get_user_service
