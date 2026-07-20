import json

from app.config import Config


def generate_ai_json(system_prompt: str, data: dict) -> dict | None:
    """Ask Gemini for a JSON object matching the shape implied by system_prompt.
    Returns None (never raises) if the API key is missing, the client can't be
    built, the call fails, or the response isn't valid JSON — callers should
    fall back to a rule-based summary in that case.
    """
    if not Config.GEMINI_API_KEY:
        return None

    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        return None

    try:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=f"Data (JSON): {data}",
            config=genai_types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=500,
                temperature=0.4,
                response_mime_type="application/json",
            ),
        )
        text = (response.text or "").strip()
        return json.loads(text) if text else None
    except Exception as exc:
        print(f"[ai_summary] generation failed (non-fatal): {exc}")
        return None
