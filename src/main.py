from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src import career_pages, users
from src.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

if settings.ENVIRONMENT == "local":
    app.mount("/static", StaticFiles(directory="static"), name="static")


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(users.router, prefix=settings.API_PREFIX_V1)
app.include_router(career_pages.router, prefix=settings.API_PREFIX_V1)
