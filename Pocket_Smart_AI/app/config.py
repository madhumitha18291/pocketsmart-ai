import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv(
        "APP_NAME",
        "PocketSmart AI"
    )

    secret_key: str = os.getenv(
        "SECRET_KEY",
        "change-this-development-secret"
    )

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/pocketsmart.db"
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    ai_enabled: bool = (
        os.getenv("AI_ENABLED", "true").lower() == "true"
    )

    session_max_age: int = int(
        os.getenv("SESSION_MAX_AGE", "86400")
    )

    max_upload_mb: int = int(
        os.getenv("MAX_UPLOAD_MB", "5")
    )


settings = Settings()
