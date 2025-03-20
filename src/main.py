from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings

app = FastAPI()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")],
):
    return {"filenames": [file.filename for file in files]}
