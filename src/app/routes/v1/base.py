from fastapi import APIRouter
from .user import user_router
from .auth import auth_router
from .user_referal import referal_router
router = APIRouter()

router.include_router(user_router, tags=['user'])
router.include_router(auth_router, tags=['jwt auth'])
router.include_router(referal_router, tags=['referal'])
