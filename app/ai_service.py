import os
import logging
from google import genai
from google.genai import types
from app.schemas import ContractCreate

logger = logging.getLogger(__name__)

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def _get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is not set.")
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    return genai.Client(api_key=api_key)


def extract_contract_data_with_ai(dirty_text: str) -> dict:
    client = _get_client()

    prompt = f"""
    You are a precision OCR and data extraction system for a renewable energy company.
    Extract the client contract data from the legacy contract text below.
    
    Rules:
    - 'pesel': exactly 10 digits (NIP) or 11 digits (PESEL), numbers only.
    - 'postal_code': format XX-XXX.
    - 'phone': phone number with or without country prefix.
    - 'email': valid email address string, or null if not found.
    - Treat references to 'VertEnergia S.A.' as template data, not customer data.
    
    Contract text:
    {dirty_text}
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ContractCreate,
            temperature=0.0,
        ),
    )

    validated_data = ContractCreate.model_validate_json(response.text)
    return validated_data.model_dump()