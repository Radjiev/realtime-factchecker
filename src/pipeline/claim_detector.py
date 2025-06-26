from __future__ import annotations

from typing import List
import time

import json

try:
    import openai
except ImportError:  # pragma: no cover - openai not installed in tests
    openai = None

PROMPT = (
    "Extract factual claims from the given text. Return each claim as a"\
    " separate bullet point. Respond with a JSON list of strings."
)


class ClaimDetector:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        if openai:
            openai.api_key = api_key

    def detect(self, text: str) -> List[str]:
        if openai is None:
            raise ImportError("openai package is required")

        attempt = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": PROMPT},
                        {"role": "user", "content": text},
                    ],
                    temperature=0,
                )
                break
            except Exception:
                attempt += 1
                if attempt >= 3:
                    raise
                time.sleep(2 ** attempt)
                continue
        content = response["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except Exception:
            # Fall back to naive parsing if JSON fails
            return [line.strip("- ") for line in content.splitlines() if line]
