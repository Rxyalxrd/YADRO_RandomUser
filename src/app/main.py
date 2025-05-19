from fastapi import FastAPI
from app.api import main_router

app = FastAPI(
    title="RandomUser Redis API",
    version="1.0.0",
    description="API для загрузки и получения случайных пользователей из Redis"
)

app.include_router(main_router)
