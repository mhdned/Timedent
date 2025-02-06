from fastapi import APIRouter

router = APIRouter()

from routes.app.auth import router as AuthRouter
from routes.app.available import router as AvailableRouter
from routes.app.course import router as CourseRouter
from routes.app.dashboard import router as DashboardRouter
from routes.app.field import router as FieldRouter
from routes.app.root import router as RootRouter
from routes.app.teacher import router as TeacherRouter
from routes.app.user import router as UserRouter

router.include_router(router=RootRouter, prefix="", tags=["ROOT"])
router.include_router(router=AuthRouter, prefix="/auth", tags=["AUTH"])
router.include_router(router=DashboardRouter, prefix="/dashboard", tags=["DASHBOARD"])
router.include_router(router=UserRouter, prefix="/user", tags=["USER"])
router.include_router(router=TeacherRouter, prefix="/teacher", tags=["TEACHER"])
router.include_router(router=FieldRouter, prefix="/field", tags=["FIELD"])
router.include_router(router=CourseRouter, prefix="/course", tags=["COURSE"])
router.include_router(router=AvailableRouter, prefix="/available", tags=["AVAILABLE"])
