from .admin import router as admin_router
from .prayers import router as prayers_router
from .auth import router as auth_router
from fastapi import APIRouter

router = APIRouter()


router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(prayers_router, prefix="/prayers", tags=["prayers"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
