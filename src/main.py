from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src import users
from src.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(users.router, prefix="/api/v1")
