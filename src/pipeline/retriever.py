from __future__ import annotations

from typing import List, Dict

try:
    import requests
except ImportError:  # pragma: no cover - requests not installed in tests
    requests = None

BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"


def search(query: str, api_key: str, k: int = 5) -> List[Dict[str, str]]:
    """Query Bing Search API and return top-k results."""
    if requests is None:
        raise ImportError("requests package is required")
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": k}
    response = requests.get(BING_ENDPOINT, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    results = []
    for item in data.get("webPages", {}).get("value", []):
        results.append({"url": item.get("url"), "snippet": item.get("snippet")})
    return results
