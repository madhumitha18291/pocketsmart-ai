import json

from typing import (
    Any,
    Optional
)

from app.config import settings

from app.services.catalog import (
    catalog_for
)


try:

    from google import genai

    from google.genai import types

except Exception:

    genai = None

    types = None


_client = None


def _get_client():

    global _client

    if (
        _client is None
        and settings.ai_enabled
        and settings.gemini_api_key
        and genai
    ):

        _client = genai.Client(
            api_key=settings.gemini_api_key
        )

    return _client


def _fallback(
    category: str,
    data: dict,
    products: list[dict],
    image_used: bool = False
):

    budget = float(
        data.get(
            "budget",
            0
        )
    )

    total = sum(
        float(product["price"])
        for product in products
    )

    remaining = max(
        0,
        budget - total
    )

    return {

        "summary":
            f"Here is a budget-aware "
            f"{category} plan based on "
            f"your inputs.",

        "budget":
            budget,

        "estimated_total":
            total,

        "remaining":
            remaining,

        "notes": [

            "Prices are illustrative "
            "catalog values, not live "
            "marketplace prices.",

            "Use the platform links to "
            "check current availability "
            "and pricing."
        ],

        "products":
            products,

        "image_analysis":

            "An outfit image was supplied "
            "for contextual matching."

            if image_used

            else None,

        "source":
            "mock-catalog-fallback"
    }


def _prompt(
    category: str,
    data: dict,
    products: list[dict]
):

    return f"""
You are PocketSmart AI,
a budget planning assistant.

Create a practical recommendation
for category: {category}.

User inputs:

{json.dumps(data, ensure_ascii=False)}

Candidate catalog:

{json.dumps(products, ensure_ascii=False)}

Important rules:

1. Stay within the user's budget.
2. Use only the products supplied
   in the candidate catalog.
3. Never invent prices.
4. Never invent URLs.
5. Do not claim prices are live.
6. Give concise practical advice.
7. For jewelry, use the supplied
   outfit image only as visual context
   if one is provided.

Return ONLY valid JSON.

Required JSON structure:

{{
    "summary": "string",
    "estimated_total": 0,
    "remaining": 0,
    "notes": [
        "string"
    ],
    "products": []
}}
"""


def _clean_json(
    text: str
) -> str:

    text = text.strip()

    if text.startswith(
        "```json"
    ):

        text = text[
            len("```json"):
        ]

    if text.startswith(
        "```"
    ):

        text = text[
            len("```"):
        ]

    if text.endswith(
        "```"
    ):

        text = text[
            :-len("```")
        ]

    return text.strip()


def generate_recommendation(
    category: str,
    data: dict,
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None
):

    products = catalog_for(
        category,
        float(data["budget"])
    )

    client = _get_client()

    if not client:

        return _fallback(
            category,
            data,
            products,
            bool(image_bytes)
        )

    try:

        prompt = _prompt(
            category,
            data,
            products
        )

        contents: list[Any] = [
            prompt
        ]

        if image_bytes and types:

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=(
                        mime_type
                        or "image/jpeg"
                    )
                )
            )

            contents[0] += """

Use the supplied outfit image
as visual context for jewelry
styling recommendations.
"""

        response = (
            client.models.generate_content(
                model=settings.gemini_model,
                contents=contents
            )
        )

        raw = response.text

        if not raw:

            raise ValueError(
                "Gemini returned an empty response."
            )

        raw = _clean_json(
            raw
        )

        result = json.loads(
            raw
        )

        if not isinstance(
            result,
            dict
        ):

            raise ValueError(
                "Gemini response is not a JSON object."
            )

        result["products"] = products

        result["budget"] = float(
            data["budget"]
        )

        result["source"] = "gemini"

        return result

    except Exception as exc:

        result = _fallback(
            category,
            data,
            products,
            bool(image_bytes)
        )

        result["ai_error"] = str(
            exc
        )[:300]

        return result