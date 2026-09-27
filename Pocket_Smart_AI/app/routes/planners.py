from fastapi import (
    APIRouter,
    File,
    Form,
    Request,
    UploadFile
)

from fastapi.responses import JSONResponse

from app.models.schemas import (
    HomeRequest,
    PartyRequest
)

from app.security import (
    require_user_id
)

from app.services.recommendations import (
    build
)


router = APIRouter()


@router.post(
    "/generate-home"
)
async def generate_home(
    request: Request,
    payload: HomeRequest
):

    user_id = require_user_id(
        request
    )

    return build(
        category="home",
        user_id=user_id,
        data=payload.model_dump()
    )


@router.post(
    "/generate-party"
)
async def generate_party(
    request: Request,
    payload: PartyRequest
):

    user_id = require_user_id(
        request
    )

    return build(
        category="party",
        user_id=user_id,
        data=payload.model_dump()
    )


@router.post(
    "/generate-jewelry"
)
async def generate_jewelry(
    request: Request,

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form(
        "elegant"
    ),

    outfit_color: str = Form(
        ""
    ),

    image: UploadFile | None = File(
        None
    )
):

    user_id = require_user_id(
        request
    )

    if budget <= 0:

        return JSONResponse(
            {
                "detail":
                    "Budget must be greater than zero."
            },
            status_code=400
        )

    image_bytes = None

    if image:

        allowed_types = {
            "image/png",
            "image/jpeg",
            "image/webp"
        }

        if image.content_type not in allowed_types:

            return JSONResponse(
                {
                    "detail":
                        "Only PNG, JPEG and WEBP images "
                        "are supported."
                },
                status_code=400
            )

        image_bytes = await image.read()

        if len(image_bytes) > 5 * 1024 * 1024:

            return JSONResponse(
                {
                    "detail":
                        "Image must be 5 MB or smaller."
                },
                status_code=400
            )

    data = {
        "budget": budget,
        "occasion": occasion.strip(),
        "style": style.strip(),
        "outfit_color":
            outfit_color.strip()
            or None
    }

    return build(
        category="jewelry",
        user_id=user_id,
        data=data,
        image_bytes=image_bytes,
        mime_type=(
            image.content_type
            if image
            else None
        )
    )