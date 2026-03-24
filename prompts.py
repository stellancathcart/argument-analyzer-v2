'''
prompts.py
'''
def get_argument_analysis_prompt(text: str) -> str:
    return f"""You are a logic and argumentation expert. Analyze the following argument and return ONLY valid JSON. Do not include any preamble, explanation, or markdown formatting - just the raw JSON object.

Argument to analyze:
{text}

Return this exact JSON structure:
{{
  "main_claim": "The central thesis or conclusion",
  "premises": [
    {{
      "text": "First premise",
      "type": "supporting",
      "order": 0
    }}
  ],
  "fallacies": [
    {{
      "type": "Name of fallacy (e.g., 'ad hominem', 'straw man', 'circular reasoning')",
      "explanation": "Why this is a fallacy",
      "confidence": 0.85
    }}
  ],
  "argument_strength": "weak|moderate|strong",
  "analysis": "Brief analysis of the argument's logical structure and validity"
}}

Rules:
1. Return ONLY the JSON object, nothing else
2. If no fallacies detected, return empty array: "fallacies": []
3. Confidence should be 0.0 to 1.0
4. Argument strength must be exactly one of: "weak", "moderate", "strong"
5. Extract all explicit and implicit premises
6. For premise type, use: "supporting", "objection", "assumption", or "conclusion"
"""
