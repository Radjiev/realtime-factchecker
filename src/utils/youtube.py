from typing import Optional
try:
    from googleapiclient.discovery import build
except ImportError:  # pragma: no cover - google-api-client not installed in tests
    build = None

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def get_transcript(video_id: str, api_key: str) -> Optional[str]:
    """Fetch transcript text for a YouTube video using the YouTube Data API v3.

    Returns ``None`` if no captions are available or on error.
    """
    if build is None:
        raise ImportError("google-api-python-client is required")
    try:
        youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)
        response = youtube.captions().list(part="id", videoId=video_id).execute()
        items = response.get("items")
        if not items:
            return None

        caption_id = items[0]["id"]
        caption = youtube.captions().download(id=caption_id).execute()
        body = caption.get("body")
        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="ignore")
        return body
    except Exception:
        # Gracefully return None on any API error
        return None
