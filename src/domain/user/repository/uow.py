from src.domain.base.interface import IUoW
from src.domain.user.repository.repo import IUserRepo


class IUserUOW(IUoW):
    users: IUserRepo
