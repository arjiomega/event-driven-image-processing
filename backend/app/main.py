from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.services.s3.service import S3Service


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.s3_service = S3Service()

    yield


settings = get_settings()

app = FastAPI(
    title="Image Processing Service",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "service": "image-processing-api",
        "status": "running",
        "version": "v1",
        "docs": "enabled",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}
