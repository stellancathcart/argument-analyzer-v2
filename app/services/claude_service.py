import time

from anthropic import Anthropic

from app.config import ANTHROPIC_API_KEY
from prompts import get_argument_analysis_prompt
from utils import (
    extract_json_from_response,
    validate_argument_analysis,
    calculate_argument_score,
)

MODEL_NAME = "claude-sonnet-4-20250514"
PROMPT_VERSION = "v1"


def analyze_argument_with_claude(text: str) -> dict:
    start = time.perf_counter()

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    try:
        prompt = get_argument_analysis_prompt(text)
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )

        raw_text = message.content[0].text
        parsed = extract_json_from_response(raw_text)
        cleaned = validate_argument_analysis(parsed)
        cleaned["score"] = calculate_argument_score(cleaned)

        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        cleaned["model_name"] = MODEL_NAME
        cleaned["prompt_version"] = PROMPT_VERSION
        cleaned["latency_ms"] = latency_ms
        cleaned["analysis_status"] = "success"
        cleaned["error_type"] = None

        return cleaned

    except Exception as e:
        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        # easiest useful version for tonight:
        raise RuntimeError(
            f"Argument analysis failed | "
            f"model={MODEL_NAME} prompt_version={PROMPT_VERSION} "
            f"latency_ms={latency_ms} error={type(e).__name__}: {e}"
        ) from e