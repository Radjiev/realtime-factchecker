from typing import Optional
try:
    from googleapiclient.discovery import build
except ImportError:  # pragma: no cover - google-api-client not installed in tests
    build = None

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def get_transcript(video_id: str, api_key: str) -> Optional[str]:
    """Fetch transcript text for a YouTube video using the YouTube Data API v3.

    Parameters
    ----------
    video_id: str
        The ID of the YouTube video.
    api_key: str
        API key for authenticating with the YouTube Data API.

    Returns
    -------
    Optional[str]
        The transcript text if available, otherwise None.
    """
    if build is None:
        raise ImportError("google-api-python-client is required")
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)
    request = youtube.captions().list(part="id", videoId=video_id)
    response = request.execute()
    items = response.get("items")
    if not items:
        return None

    caption_id = items[0]["id"]
    caption_request = youtube.captions().download(id=caption_id)
    caption = caption_request.execute()
    return caption.get("body")
