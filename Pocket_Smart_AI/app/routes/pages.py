from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db import get_db

from app.security import (
    user_id_from_request
)

from app.services.recommendations import (
    get_history
)


templates = Jinja2Templates(
    directory="templates"
)


router = APIRouter()


async def current_user(
    request: Request
):

    user_id = user_id_from_request(
        request
    )

    if not user_id:
        return None

    with get_db() as db:

        row = db.execute(
            """
            SELECT
                id,
                name,
                email
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

    if not row:
        return None

    return dict(row)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    user = await current_user(
        request
    )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "user": user
        }
    )


@router.get(
    "/register",
    response_class=HTMLResponse
)
async def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(
    request: Request
):

    user = await current_user(
        request
    )

    if not user:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "message":
                    "Please login first."
            }
        )

    history = get_history(
        user["id"],
        10
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "history": history
        }
    )


@router.get(
    "/planner/{category}",
    response_class=HTMLResponse
)
async def planner(
    request: Request,
    category: str
):

    user = await current_user(
        request
    )

    if not user:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "message":
                    "Please login first."
            }
        )

    if category not in {
        "home",
        "party",
        "jewelry"
    }:

        category = "home"

    return templates.TemplateResponse(
        request=request,
        name=f"{category}_planner.html",
        context={
            "user": user,
            "category": category
        }
    )


@router.get(
    "/history",
    response_class=HTMLResponse
)
async def history(
    request: Request
):

    user = await current_user(
        request
    )

    if not user:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "message":
                    "Please login first."
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "user": user,
            "history":
                get_history(
                    user["id"],
                    50
                )
        }
    )