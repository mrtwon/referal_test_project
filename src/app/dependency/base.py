from fastapi import FastAPI

from .di_user import di_user
from .di_setup import di_setup
from .di_user_referal import di_user_referal


def di_all(app: FastAPI):
    di_setup(app)
    di_user(app)
    di_user_referal(app)
