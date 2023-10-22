from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from models import Base, session
from routers.question import question_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Простой веб-сервис (с помощью FastAPI или Flask, например)", lifespan=lifespan)
app.include_router(router=question_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
