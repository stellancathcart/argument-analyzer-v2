'''
utils.py
'''

import json
import re
from typing import Any, Dict


def extract_json_from_response(text: str) -> Dict[str, Any]:
    text = text.strip()

    json_fence_pattern = r'```json\s*(\{.*?\})\s*```'
    match = re.search(json_fence_pattern, text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    fence_pattern = r'```\s*(\{.*?\})\s*```'
    match = re.search(fence_pattern, text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    json_pattern = r'\{.*\}'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Could not extract valid JSON from response: {text[:200]}...")


def validate_argument_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    if "main_claim" not in data:
        raise ValueError("Missing required field: main_claim")

    if "premises" not in data:
        data["premises"] = []

    if "fallacies" not in data:
        data["fallacies"] = []

    valid_strengths = ["weak", "moderate", "strong"]
    if "argument_strength" in data:
        if data["argument_strength"] not in valid_strengths:
            strength_lower = data["argument_strength"].lower()
            if "weak" in strength_lower:
                data["argument_strength"] = "weak"
            elif "strong" in strength_lower:
                data["argument_strength"] = "strong"
            else:
                data["argument_strength"] = "moderate"
    else:
        data["argument_strength"] = "moderate"

    if "analysis" not in data:
        data["analysis"] = "No analysis provided"

    cleaned_premises = []
    for i, premise in enumerate(data["premises"]):
        if isinstance(premise, str):
            premise = {"text": premise, "type": "supporting", "order": i}
        elif isinstance(premise, dict):
            if "text" not in premise:
                continue
            premise.setdefault("type", "supporting")
            premise.setdefault("order", i)
        cleaned_premises.append(premise)

    data["premises"] = cleaned_premises

    cleaned_fallacies = []
    for fallacy in data["fallacies"]:
        if isinstance(fallacy, dict) and "type" in fallacy:
            fallacy.setdefault("explanation", "")
            fallacy.setdefault("confidence", 0.5)
            cleaned_fallacies.append(fallacy)

    data["fallacies"] = cleaned_fallacies
    return data


def calculate_argument_score(data: Dict[str, Any]) -> float:
    strength_scores = {
        "weak": 30,
        "moderate": 60,
        "strong": 90,
    }
    score = strength_scores.get(data["argument_strength"], 50)
    score -= len(data["fallacies"]) * 10
    score += min(len(data["premises"]), 3) * 5
    return max(0, min(100, score))
