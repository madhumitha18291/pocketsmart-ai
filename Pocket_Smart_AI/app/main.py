from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.staticfiles import (
    StaticFiles
)

from app.config import settings

from app.db import init_db

from app.routes import (
    auth,
    pages,
    planners
)


@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    init_db()

    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered budget and "
        "recommendation assistant."
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)


app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router,
    prefix="/api"
)

app.include_router(
    planners.router,
    prefix="/api"
)


@app.get("/health")
async def health():

    return {
        "status": "ok",

        "app":
            settings.app_name,

        "ai_enabled":
            bool(
                settings.ai_enabled
                and settings.gemini_api_key
            )
    }


@app.get("/startup")
async def startup():

    return {
        "status": "ready"
    }


@app.get(
    "/recommendations-details"
)
async def recommendations_details():

    return {
        "detail":
            "Use the planner endpoints "
            "to generate recommendations."
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )