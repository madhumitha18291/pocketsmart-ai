import json

from app.db import get_db

from app.services.gemini_utils import (
    generate_recommendation
)


def save_recommendation(
    user_id: int,
    category: str,
    budget: float,
    request_data: dict,
    result: dict
):

    with get_db() as db:

        db.execute(
            """
            INSERT INTO recommendations
            (
                user_id,
                category,
                budget,
                request_json,
                response_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,

                category,

                budget,

                json.dumps(
                    request_data,
                    ensure_ascii=False
                ),

                json.dumps(
                    result,
                    ensure_ascii=False
                )
            )
        )


def get_history(
    user_id: int,
    limit: int = 30
):

    with get_db() as db:

        rows = db.execute(
            """
            SELECT *
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                user_id,
                limit
            )
        ).fetchall()

    return [
        dict(row)
        for row in rows
    ]


def build(
    category: str,
    user_id: int,
    data: dict,
    image_bytes=None,
    mime_type=None
):

    result = generate_recommendation(
        category=category,
        data=data,
        image_bytes=image_bytes,
        mime_type=mime_type
    )

    save_recommendation(
        user_id=user_id,
        category=category,
        budget=float(
            data["budget"]
        ),
        request_data=data,
        result=result
    )

    return result