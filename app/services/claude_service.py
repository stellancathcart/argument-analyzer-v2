from anthropic import Anthropic

from app.config import ANTHROPIC_API_KEY
from prompts import get_argument_analysis_prompt
from utils import (
    extract_json_from_response,
    validate_argument_analysis,
    calculate_argument_score,
)


def analyze_argument_with_claude(text: str) -> dict:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = get_argument_analysis_prompt(text)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = message.content[0].text
    parsed = extract_json_from_response(raw_text)
    cleaned = validate_argument_analysis(parsed)
    cleaned["score"] = calculate_argument_score(cleaned)
    return cleaned