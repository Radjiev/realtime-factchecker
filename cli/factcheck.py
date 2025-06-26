import re
from pathlib import Path
from typing import List

import typer

from src.utils.youtube import get_transcript
from src.pipeline.claim_detector import ClaimDetector
from src.pipeline.retriever import search
from src.pipeline.scorer import FactCheckScorer
from src.pipeline.caption_builder import build_webvtt

app = typer.Typer()

YOUTUBE_RE = re.compile(r"v=([^&]+)")


def extract_video_id(url: str) -> str:
    match = YOUTUBE_RE.search(url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)


@app.command()
def factcheck(youtube_url: str, out: Path):
    """Run fact checking pipeline on a YouTube video."""
    video_id = extract_video_id(youtube_url)
    api_key = "YOUR_YOUTUBE_API_KEY"
    transcript = get_transcript(video_id, api_key) or ""

    claim_detector = ClaimDetector(api_key="OPENAI_API_KEY")
    claims = claim_detector.detect(transcript)

    scorer = FactCheckScorer(api_key="OPENAI_API_KEY")

    segments: List[dict] = []
    for idx, claim in enumerate(claims):
        results = search(claim, api_key="BING_API_KEY")
        snippets = [r["snippet"] for r in results]
        score = scorer.score(claim, snippets)
        segments.append(
            {
                "start": "00:00:00.000",
                "end": "00:00:05.000",
                "text": claim,
                "label": score.get("label"),
                "confidence": float(score.get("confidence", 0)),
            }
        )

    vtt = build_webvtt(segments)
    out.write_text(vtt)
    typer.echo(f"Wrote {out}")


if __name__ == "__main__":
    app()
