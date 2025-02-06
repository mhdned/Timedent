from fastapi import APIRouter, Depends

router = APIRouter()

from middlewares.auth import auth_admin
from routes.admin.auth import router as AuthRouter
from routes.admin.dashboard import router as DashboardRouter
from routes.admin.log import router as LogRouter

router.include_router(router=LogRouter, prefix="/log", tags=["LOG"])
router.include_router(router=AuthRouter, prefix="/auth", tags=["AUTH"])
router.include_router(
    router=DashboardRouter,
    prefix="/dashboard",
    tags=["DASHBOARD"],
    dependencies=[Depends(auth_admin)],
)
