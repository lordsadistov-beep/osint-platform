from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .lessons import router as lessons_router
from .challenges import router as challenges_router
from .dashboard import router as dashboard_router
from .tools.username import router as username_router
from .tools.email_checker import router as email_router
from .tools.phone_checker import router as phone_router
from .tools.domain_tool import router as domain_router
from .tools.leaks import router as leaks_router
from .tools.metadata import router as metadata_router
from .tools.graph import router as graph_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(lessons_router, prefix="/lessons", tags=["Lessons"])
api_router.include_router(challenges_router, prefix="/challenges", tags=["Challenges"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(username_router, prefix="/tools", tags=["Tools"])
api_router.include_router(email_router, prefix="/tools", tags=["Tools"])
api_router.include_router(phone_router, prefix="/tools", tags=["Tools"])
api_router.include_router(domain_router, prefix="/tools", tags=["Tools"])
api_router.include_router(leaks_router, prefix="/tools", tags=["Tools"])
api_router.include_router(metadata_router, prefix="/tools", tags=["Tools"])
api_router.include_router(graph_router, prefix="/tools", tags=["Tools"])
