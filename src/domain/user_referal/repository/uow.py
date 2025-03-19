from src.domain.base.interface import IUoW
from src.domain.user_referal.repository.repo import IUserReferalRepo


class IUserReferalUOW(IUoW):
    user_referal: IUserReferalRepo