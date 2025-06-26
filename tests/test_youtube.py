import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[1] / "src/utils/youtube.py"
spec = importlib.util.spec_from_file_location("youtube", module_path)
youtube_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(youtube_module)
get_transcript = youtube_module.get_transcript


def test_get_transcript_signature():
    assert callable(get_transcript)
