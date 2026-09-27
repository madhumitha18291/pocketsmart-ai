from typing import Literal, Optional

from pydantic import BaseModel, Field


Category = Literal[
    "home",
    "party",
    "jewelry"
]


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: str = Field(
        min_length=5,
        max_length=160
    )

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: str

    password: str


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    room: str = Field(
        min_length=2,
        max_length=60
    )

    style: str = Field(
        default="modern",
        max_length=80
    )

    items: str = Field(
        default="lights, decor, furniture",
        max_length=300
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    venue: str = Field(
        default="home or affordable hall",
        max_length=120
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    occasion: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        default="elegant",
        max_length=80
    )

    outfit_color: Optional[str] = Field(
        default=None,
        max_length=80
    )