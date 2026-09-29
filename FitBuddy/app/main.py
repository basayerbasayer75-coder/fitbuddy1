from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes import router
@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db();yield
app=FastAPI(title='FitBuddy – AI Fitness Plan Generator',version='1.0.0')
base=Path(__file__).resolve().parent.parent
app.mount('/static',StaticFiles(directory=str(base/'static')),name='static')
app.include_router(router)
app.router.lifespan_context=lifespan
