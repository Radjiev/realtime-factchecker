from __future__ import annotations

from typing import List, Dict
import json

try:
    import openai
except ImportError:  # pragma: no cover - openai not installed in tests
    openai = None

PROMPT_TEMPLATE = (
    "Given a factual claim and a list of evidence snippets, determine whether "
    "the claim is true, false, or unverified based on the evidence. "
    "Respond with JSON containing 'label' (true/false/unverified) and "
    "'confidence' (0-1)."
)


class FactCheckScorer:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        if openai:
            openai.api_key = api_key

    def score(self, claim: str, evidence: List[str]) -> Dict[str, str]:
        if openai is None:
            raise ImportError("openai package is required")
        messages = [
            {"role": "system", "content": PROMPT_TEMPLATE},
            {
                "role": "user",
                "content": json.dumps({"claim": claim, "evidence": evidence}),
            },
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0,
        )
        content = response["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except Exception:
            return {"label": "unverified", "confidence": 0.0}
