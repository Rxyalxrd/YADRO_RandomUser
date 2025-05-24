from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import main_router
from app.services.user_loader import load_users
from app.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await load_users(limit=1000)

    yield


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    lifespan=lifespan,
    description=settings.app_description,
)


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main_router)
