import base64
import hashlib
import hmac
import os

from datetime import datetime, timedelta, timezone

import jwt

from fastapi import HTTPException, Request

from app.config import settings


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    """

    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        210_000
    )

    encoded = base64.b64encode(
        salt + digest
    ).decode("utf-8")

    return encoded


def verify_password(
    password: str,
    encoded_password: str
) -> bool:

    try:
        raw = base64.b64decode(
            encoded_password.encode("utf-8")
        )

        salt = raw[:16]

        expected = raw[16:]

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            210_000
        )

        return hmac.compare_digest(
            actual,
            expected
        )

    except Exception:
        return False


def create_token(user_id: int) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(
            seconds=settings.session_max_age
        )
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM
    )


def user_id_from_request(
    request: Request
):

    token = request.cookies.get(
        "access_token"
    )

    if not token:
        return None

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )

        return int(payload["sub"])

    except Exception:

        return None


def require_user_id(
    request: Request
) -> int:

    user_id = user_id_from_request(
        request
    )

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Login required."
        )

    return user_id