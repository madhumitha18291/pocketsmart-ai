import re

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.db import get_db

from app.security import (
    create_token,
    hash_password,
    user_id_from_request,
    verify_password
)


router = APIRouter()


EMAIL_REGEX = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


@router.post("/register")
async def register(payload: dict):

    name = payload.get(
        "name",
        ""
    ).strip()

    email = payload.get(
        "email",
        ""
    ).strip().lower()

    password = payload.get(
        "password",
        ""
    )

    if (
        len(name) < 2
        or not EMAIL_REGEX.match(email)
        or len(password) < 6
    ):

        return JSONResponse(
            {
                "detail":
                    "Enter a valid name, email and "
                    "password with at least 6 characters."
            },
            status_code=400
        )

    try:

        with get_db() as db:

            cursor = db.execute(
                """
                INSERT INTO users
                (name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    hash_password(password)
                )
            )

            user_id = cursor.lastrowid

    except Exception:

        return JSONResponse(
            {
                "detail":
                    "An account with this email "
                    "already exists."
            },
            status_code=409
        )

    token = create_token(
        user_id
    )

    response = JSONResponse(
        {
            "ok": True,
            "user": {
                "id": user_id,
                "name": name,
                "email": email
            }
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=86400
    )

    return response


@router.post("/login")
async def login(payload: dict):

    email = payload.get(
        "email",
        ""
    ).strip().lower()

    password = payload.get(
        "password",
        ""
    )

    with get_db() as db:

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

    if (
        not user
        or not verify_password(
            password,
            user["password_hash"]
        )
    ):

        return JSONResponse(
            {
                "detail":
                    "Invalid email or password."
            },
            status_code=401
        )

    token = create_token(
        user["id"]
    )

    response = JSONResponse(
        {
            "ok": True,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=86400
    )

    return response


@router.post("/logout")
async def logout():

    response = JSONResponse(
        {"ok": True}
    )

    response.delete_cookie(
        "access_token"
    )

    return response


@router.get("/session-info")
async def session_info(
    request: Request
):

    user_id = user_id_from_request(
        request
    )

    if not user_id:

        return {
            "authenticated": False
        }

    with get_db() as db:

        user = db.execute(
            """
            SELECT
                id,
                name,
                email,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

    return {
        "authenticated": bool(user),
        "user": dict(user)
        if user
        else None
    }


@router.get("/session-data")
async def session_data(
    request: Request
):

    user_id = user_id_from_request(
        request
    )

    if not user_id:

        return JSONResponse(
            {
                "detail":
                    "Login required."
            },
            status_code=401
        )

    with get_db() as db:

        row = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM recommendations
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

    return {
        "recommendation_count":
            row["count"]
    }