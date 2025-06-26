from __future__ import annotations

from typing import Iterable, Dict


def build_webvtt(segments: Iterable[Dict[str, str]]) -> str:
    """Build WebVTT captions from segments.

    Each segment dict must contain: start, end, text, label, confidence.
    """
    lines = ["WEBVTT\n"]
    for i, seg in enumerate(segments, start=1):
        lines.append(f"{i}")
        lines.append(f"{seg['start']} --> {seg['end']}")
        text = seg["text"]
        label = seg.get("label")
        conf = seg.get("confidence")
        lines.append(f"{text} ({label}, {conf:.2f})\n")
    return "\n".join(lines)
