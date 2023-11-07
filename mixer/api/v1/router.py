from fastapi import APIRouter

from core.main import app

mixer_router = APIRouter(prefix="mixer")

app.include_router(mixer_router, prefix="v1")
