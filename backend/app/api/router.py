from fastapi import APIRouter

from .media.router import router as media_router

api_router = APIRouter()
api_router.include_router(media_router)
