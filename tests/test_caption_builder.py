import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[1] / "src/pipeline/caption_builder.py"
spec = importlib.util.spec_from_file_location("caption_builder", module_path)
caption_builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(caption_builder)
build_webvtt = caption_builder.build_webvtt


def test_build_webvtt_basic():
    segments = [
        {"start": "00:00:00.000", "end": "00:00:01.000", "text": "test", "label": "true", "confidence": 1.0}
    ]
    vtt = build_webvtt(segments)
    assert "WEBVTT" in vtt
